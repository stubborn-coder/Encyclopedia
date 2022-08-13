from audioop import reverse
from logging import PlaceHolder
from django.shortcuts import render
from django import forms 
from django.urls import reverse
from django.http import HttpResponseRedirect

from . import util
import encyclopedia
from random import randrange
from markdown2 import Markdown

class NewPageForm(forms.Form):
    title = forms.CharField(label="title",initial="")
    content = forms.CharField(widget=forms.Textarea(attrs={'name':'content'}),label="content")


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def layout(request):
    return render(request,"encyclopedia/layout.html")

def entry(request,name):
    markdowner = Markdown()
    markdown = markdowner.convert(util.get_entry(name))
    #markdown = html.escape(markdown)
    if markdown == None:
        return render(request,"encyclopedia/error.html")
    else:
        return render(request,"encyclopedia/entry.html",{
            'entry_name' : name,
            'entry_data' : markdown
        })

def create(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content =form.cleaned_data["content"]
            if util.get_entry(title) == None:
                util.save_entry(title,content)
                return HttpResponseRedirect(entry(request,title))
            else:
                return render(request,"encyclopedia/create.html",{
                    "form" : form
                })

    return render(request,"encyclopedia/create.html",{
        "form" : NewPageForm()
    })

def randompage(request):
    list_of_entries = util.list_entries()
    random_index = randrange(0,len(list_of_entries))
    random_entry = list_of_entries[random_index]
    return HttpResponseRedirect(random_entry)

def editentry(request,name):

    if util.get_entry(name) is not None:
        
        content = util.get_entry(name)
        title = name
        data = {"title" : title , "content" : content}
        form = NewPageForm(data)
        
        return render(request,"encyclopedia/edit.html",{
            "form" : form
        })
    else:
        render(request,"encyclopedia/edit.html",{
            "form": NewPageForm()
        })


def save(request):

    if request.method == "POST":
        form = NewPageForm(request.POST)

        if form.is_valid():
            title = form.cleaned_data["title"]
            content =form.cleaned_data["content"]
            util.save_entry(title,content)
            return entry(request,title)

def search(request):
    search_query = request.GET.get('q')
    if util.get_entry(search_query) is not None:
        return entry(request,search_query)
    else:
        list_of_entries = util.list_entries()
        search_results = []
        for entry in list_of_entries:
            if search_query in entry:
                search_results.append(entry)
        return render(request,"encyclopedia/index.html",{
            "entries" : search_results
        })

