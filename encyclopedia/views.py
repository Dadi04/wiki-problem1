from django.shortcuts import render
from django.http import HttpResponseRedirect, HttpResponse
from django.urls import reverse
import random

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, name):
    for names in util.list_entries():
        if name in names:
            return render(request, "encyclopedia/entry.html", {
                "entry": markdown2.markdown(util.get_entry(name)),
                "title": name
            })
    return HttpResponse("The page you are looking for does not exist!") 

def search(request):
    entries = util.list_entries()
    text = request.GET.get("q", "")
    if text in entries:
        return HttpResponseRedirect(reverse("entry", kwargs={"name":text}))
    results = [entry for entry in entries if text.lower() in entry.lower()]
    return render(request, "encyclopedia/search_results.html", {
        "entries": results
    })

def new_page(request):
    if request.method == "POST":
        title = request.POST.get("title", "")
        content = request.POST.get("content", "")
        if title in util.list_entries():
            return HttpResponse(f"{title} already exists")
        else:
            util.save_entry(title, content)
            new_content = markdown2.markdown(util.get_entry(title))
            return render(request, "encyclopedia/entry.html", {
                    "title": title,
                    "entry": new_content
                })
    else:
        return render(request, "encyclopedia/new_page.html")
    
def edit_page(request, name):
    return render(request, "encyclopedia/edit_page.html", {
        "content": util.get_entry(name),
        "title": name
    })

def submit(request, name):
    util.save_entry(name, bytes(request.POST.get("textarea"),'utf8'))
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(name)),
        "title": name
    })

def random_page(request):
    randomise = random.choice(util.list_entries())
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(randomise)),
        "title": randomise
    })