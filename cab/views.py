import sys
import logging
from django.urls import reverse
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponseRedirect, HttpResponseForbidden

# ? Current Active User Model
User = get_user_model()


logger = logging.getLogger(__name__)

# ? Import Local Models
from .models import (
    Snippet,
    Language,
    Bookmark,
    Rating
)

# ? Import Local Forms
from .forms import(
    SnippetForm
)

# ? Create your views here.

def index(request):
    template_name = 'cab/index.html'
    context = {
    }
    return render(request, template_name, context)


def SnippetLists(request):
    template_name = 'cab/snippet_list.html'
    snippets = Snippet.objects.all()
    context = {
        "snippets": snippets
    }
    return render(request, template_name, context)


def snippetDetail(request, snippet_id):
    template_name = 'cab/snippet_detail.html'
    try:
        snippet = Snippet.objects.get(id=snippet_id)
    except Snippet.DoesNotExist:
        messages.error(request, "Requested Snippet Does Not Exist.")
        return redirect(reverse("index"))
    except Exception as e:
        logger.error(e, exc_info=sys.exc_info())
        messages.error(
            request, "There might be some error caught. Try again after some time.")
        return redirect(reverse("index"))
    context = {
        "snippet": snippet
    }
    return render(request, template_name, context)


def languageList(request):
    template_name = 'cab/language_list.html'
    all_languages = Language.top_objects.top_languages()
    # print(all_languages)
    context = {
        "all_languages": all_languages
    }
    return render(request, template_name, context)


def languageDetail(request, slug_lang):
    template_name = 'cab/language_detail.html'
    try:
        lang = Language.objects.get(slug=slug_lang)
        snippets = lang.snippet_set.all()
    except Language.DoesNotExist:
        messages.error(request, "Requested Page Does Not Exist.")
        return redirect(reverse("index"))
    except Exception as e:
        logger.error(e, exc_info=sys.exc_info())
        messages.error(
            request, "There might be some error caught. Try again after some time.")
        return redirect(reverse("index"))
    context = {
        "snippets": snippets,
        "lang": lang
    }
    return render(request, template_name, context)


def authorList(request):
    template_name = 'cab/top_authors.html'
    all_authors = Snippet.score_objects.top_authors()
    context = {
        "all_authors": all_authors
    }
    return render(request, template_name, context)


@login_required
def add_snippet(request):
    template_name = "cab/add_snippet.html"
    if request.method == 'POST':
        form = SnippetForm(data=request.POST)
        if form.is_valid():
            new_snippet = form.save(commit=False)
            new_snippet.author = request.user
            new_snippet.save()
            return HttpResponseRedirect(new_snippet.get_absolute_url())
    else:
        form = SnippetForm()
    context = {
        'form': form
    }
    return render(request, template_name, context)


@login_required
def edit_snippet(request, snippet_id):
    template_name = 'cab/edit_snippet.html'
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.user.id != snippet.author.id:
        return HttpResponseForbidden()
    if request.method == 'POST':
        form = SnippetForm(instance=snippet, data=request.POST)
        if form.is_valid():
            snippet = form.save()
            return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        form = SnippetForm(instance=snippet)
    context = {'form': form, 'add': False}
    return render(request, template_name, context)


@login_required
def add_bookmark(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    try:
        Bookmark.objects.get(user__pk=request.user.id,snippet__pk=snippet.id)
        messages.info(request, "Already Bookmarked")
    except Bookmark.DoesNotExist:
        Bookmark.objects.create(user=request.user, snippet=snippet)
        messages.success(request, "Successfully Bookmarked")
    return HttpResponseRedirect(snippet.get_absolute_url())


@login_required
def delete_bookmark(request, snippet_id):
    template_name="cab/confirm_bookmark_delete.html"
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if request.method == 'POST':
        Bookmark.objects.filter(user__pk=request.user.id, snippet__pk=snippet.id).delete()
        return HttpResponseRedirect(snippet.get_absolute_url())
    else:
        context= { 'snippet': snippet }
        return render(request, template_name, context)

@login_required
def user_bookmarks(request):
    template_name = 'cab/user_bookmark_list.html'
    user_bookmark_list = Bookmark.objects.filter(user = request.user)
    context = {
        "user_bookmark_list" : user_bookmark_list
    }
    return render(request, template_name, context)


def most_bookmarked(request):
    template_name='cab/most_bookmarked.html'
    bookmark_list = Snippet.score_objects.most_bookmarked()
    context = {
        "bookmark_list" : bookmark_list
    }
    return render(request, template_name, context)


@login_required
def rateAdd(request, snippet_id):
    snippet = get_object_or_404(Snippet, pk=snippet_id)
    if 'rating' not in request.GET or request.GET['rating'] not in ('1', '-1'):
        return HttpResponseRedirect(snippet.get_absolute_url())
    try:
        rating = Rating.objects.get(user__pk=request.user.id, snippet__pk=snippet.id)
    except Rating.DoesNotExist:
        rating = Rating(user=request.user, snippet=snippet)
    rating.rating = int(request.GET['rating'])
    rating.save()
    return HttpResponseRedirect(snippet.get_absolute_url())