from django.shortcuts import HttpResponseRedirect, render
from django.urls import reverse
from markdown2 import markdown
import random

from . import util


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry(request, title):
    content = util.get_entry(title)

    if content is None:
        return render(request, "encyclopedia/errorSearch.html", {
            "title": title,
            "message": "Error",
        })
    return render(request, "encyclopedia/entry.html", {
        "title": title,
        "content": markdown(content)
    })



def search(request):
    query = request.GET.get("q")
    entries = util.list_entries()

    if util.get_entry(query):
        return HttpResponseRedirect(reverse("entry", args=[query]))
    
    results = [entry for entry in entries if query.lower() in entry.lower()]

    return render(request, "encyclopedia/search.html", {
        "title": query,
        "results": results,
        "query": query
    })



def create(request):
    if request.method == "POST":
        title = request.POST["title"]
        content = request.POST["content"]
        if util.get_entry(title):
            return render(request, "encyclopedia/errorCreate.html", {
                "title": title
            })
        
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
    return render(request, "encyclopedia/create.html")



def edit(request, title):
    if request.method == "POST":
        content = request.POST["content"]
        util.save_entry(title, content)
        return HttpResponseRedirect(reverse("entry", args=[title]))
    
    content = util.get_entry(title)
    return render(request, 'encyclopedia/edit.html', {
        "title": title,
        "content": content.rstrip()
    })



def random_page(request):
    entries = util.list_entries()
    title = random.choice(entries)
    return HttpResponseRedirect(reverse("entry", args=[title]))