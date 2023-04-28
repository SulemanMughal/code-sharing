from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('all-snippets/', views.SnippetLists, name="cab_snippet_list"),
    path('snippet/<int:snippet_id>', views.snippetDetail, name="cab_snippet_detail"),
    path("languages", views.languageList, name="cab_language_list"),
    path("languages/<slug:slug_lang>", views.languageDetail, name="cab_language_detail"),
    path("author", views.authorList, name="cab_author_list"),
    path("add-snippet", views.add_snippet,name="cab_snippet_add"),
    path("edit-snippet/<int:snippet_id>", views.edit_snippet, name="cab_snippet_edit"),
    path("add-bookmark/<int:snippet_id>/", views.add_bookmark, name="cab_bookmark_add"),
    path("delete-bookmark/<int:snippet_id>/", views.delete_bookmark, name="cab_bookmark_delete"),
    path("user-bookmarks", views.user_bookmarks, name="cab_user_bookmarks"),
    path("add-rating/<int:snippet_id>/", views.rateAdd,name="cab_rating_add"),

]