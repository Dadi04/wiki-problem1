from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.urls import reverse

from . import util

import markdown2


def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries(),
    })

def entry(request, name):
    return render(request, "encyclopedia/entry.html", {
        "entry": markdown2.markdown(util.get_entry(name)),
        "title": name
    })

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
        util.save_entry(title, content)
        return render(request, "encyclopedia/entry.html", {
            "title": title,
            "entry": content
        })
    else:
        return render(request, "encyclopedia/new_page.html")