import datetime
from pyexpat import model
from django.db import models
from django.urls import reverse
from django.contrib.auth import get_user_model


from django.utils.translation import gettext_lazy as _

# ? Current Active User Model
User = get_user_model()

# ? Import Local Manager
from . import managers


# ? Third-Party Imports
# from pygments import lexers
from pygments import (
    formatters, 
    highlight, 
    lexers
)
from tagging.fields import TagField
from markdown import markdown

# Create your models here.

class Language(models.Model):
    name = models.CharField(max_length=100, help_text = _("The name of the language"))
    slug = models.SlugField(unique=True , help_text = _("A unique slug to identify it in URLs"))
    language_code = models.CharField(max_length=50 , help_text = _("A language code that pygments can use to load the appropriate syntax-highlighting module"))
    mime_type = models.CharField(max_length=100 , help_text = _("A MIME type to use when sending a snippet file in this language"))


    # ? Managers
    objects = models.Manager()
    top_objects = managers.LanguageManager()

    class Meta:
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('cab_language_detail', args=[self.slug])

    def get_lexer(self):
        return lexers.get_lexer_by_name(self.language_code)

    

    

class Snippet(models.Model):
    title = models.CharField(max_length=255)
    language = models.ForeignKey(Language, on_delete=models.CASCADE , help_text= _("A foreign key pointing at the Language the snippet is written in"))
    author = models.ForeignKey(User, on_delete=models.CASCADE, help_text = _("A foreign key to Django’s User model to represent the snippet’s author."))
    description = models.TextField()
    description_html = models.TextField(editable=False)
    code = models.TextField(help_text=_("The actual code"))
    highlighted_code = models.TextField(editable=False, help_text=_("Syntax-highlighted HTML version separate from the original code"))
    tags = TagField( help_text=_("A list of tags"))
    pub_date = models.DateTimeField(editable=False, help_text=_("The date and time when the snippet was first posted"))
    updated_date = models.DateTimeField(editable=False, help_text=_("The date and time when it was last updated"))


    class Meta:
        ordering = ['-pub_date']


    # ? Managers
    objects = models.Manager()
    score_objects = managers.SnippetManager()

    def __str__(self):
        return self.title

    def highlight(self):
        return highlight(
            self.code,
            self.language.get_lexer(),
            formatters.HtmlFormatter(linenos=True)
        )

    def save(self):
        if not self.id:
            self.pub_date = datetime.datetime.now()
        self.updated_date = datetime.datetime.now()
        self.description_html = markdown(self.description)
        self.highlighted_code = self.highlight()
        super(Snippet, self).save()

    def get_absolute_url(self):
        return reverse('cab_snippet_detail', args=[self.id])


class Bookmark(models.Model):
    snippet = models.ForeignKey(Snippet , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='cab_bookmarks' , on_delete=models.CASCADE)
    date = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        ordering = ['-date']

    def __str__(self):
        return "%s bookmarked by %s" % (self.snippet, self.user)


class Rating(models.Model):
    RATING_UP = 1
    RATING_DOWN = -1
    RATING_CHOICES = ((RATING_UP, 'useful'),
    (RATING_DOWN, 'not useful'))
    snippet = models.ForeignKey(Snippet , on_delete=models.CASCADE)
    user = models.ForeignKey(User, related_name='cab_rating', on_delete=models.CASCADE)
    rating = models.IntegerField(choices=RATING_CHOICES)
    date = models.DateTimeField(auto_now_add = True)

    def __str__(self):
        return "%s rating %s (%s)" % (self.user, self.snippet,
        self.get_rating_display())