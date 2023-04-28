from django.db import models
from django.db import connection
from django.contrib.auth import get_user_model

# ? Current Active User Model
User = get_user_model()

class SnippetManager(models.Manager):
    # def top_authors(self):
    #     return User.objects.extra(select={ 'score': "SELECT COUNT(*) from cab_snippet WHERE cab_snippet.author_id =auth_user.id" }, order_by=['-score'])

    def top_authors(self):
        subquery = "SELECT COUNT(*) from %(snippets_table)s WHERE %(snippets_table)s.%(author_column)s = auth_user.id"
        params = { 'snippets_table': connection.ops.quote_name( self.model._meta.db_table),
        'author_column': connection.ops.quote_name('author_id') }
        return User.objects.extra(select={ 'score': subquery % params }, order_by=['-score'])

    def most_bookmarked(self):
        from cab.models import Bookmark
        subquery = "SELECT COUNT(*) from %(bookmarks_table)s WHERE %(bookmarks_table)s.%(snippet_column)s = snippet.id"
        params = { 'bookmarks_table':connection.ops.quote_name(Bookmark._meta.db_table), 'snippet_column': connection.ops.quote_name('snippet_id') }
        return self.extra(select={ 'score': subquery % params }, order_by=['-score'])

    def top_rated(self):
        from cab.models import Rating
        subquery = "SELECT SUM(%(rating_column)s) from %(rating_table)s WHERE %(rating_table)s.%(snippet_column)s = snippet.id"
        params = { 'rating_column': connection.ops.quote_name('rating'),
        'rating_table': connection.ops.quote_name(Rating._meta.db_table),
        'snippet_column': connection.ops.quote_name('snippet_id') }
        return self.extra(select={ 'score': subquery % params }, order_by=['-score'])


class LanguageManager(models.Manager):
    def top_languages(self):
        from cab.models import Snippet
        subquery = "SELECT COUNT(*) from %(snippets_table)s WHERE %(snippets_table)s.%(language_column)s = cab_language.id" 
        params = { 'snippets_table': connection.ops.quote_name( Snippet._meta.db_table), 'language_column': connection.ops.quote_name('language_id') }
        return self.extra(select={ 'score': subquery % params }, order_by=['-score'])