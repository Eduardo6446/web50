from django import forms
from django.shortcuts import render, redirect
from django.http import Http404
from . import util
from markdown2 import Markdown
from django.contrib import messages

class CreateForm(forms.Form):
    title = forms.CharField(
        required=True,
        label="",
        widget=forms.TextInput(
            attrs={"placeholder": "Title", "class": "mb-4"}
        ),
    )
    content = forms.CharField(
        required=True,
        label="",
        widget=forms.Textarea(
            attrs={
                "class": "form-control mb-4",
                "placeholder": "Input something (Markdown) ... ",
                "id": "new_content",
            }
        ),
    )

def index(request):

    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def entry_page(request, title):

    if title not in util.list_entries():
        raise Http404

    entry = util.get_entry(title)
    return render(request, "encyclopedia/entry.html", {"title": title, "content": Markdown().convert(entry)})

def search(request):
    query = request.GET.get("q", "")
    if query is None or query == "":
        return render(
            request,
            "encyclopedia/search.html",
            {"matches": "", "query": query},
        )

    entries = util.list_entries()
    
    matches = [
        entry
        for entry in entries
        if query.lower() in entry.lower()
    ]
    if len(matches) == 1:
        return redirect('entry', matches[0])

    return render(
        request,
        "encyclopedia/search.html",
        {"matches": matches, "query": query},
    )

def create_new_page(request):
    if request.method == "POST":
        form = CreateForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data.get("title")
            content = form.cleaned_data.get("content")
            print(title)

            if util.get_entry(title):
                messages.error(request, 'This page already exists!')
                return redirect('create')
            else:
                util.save_entry(title, content)
                messages.success(request, f'New page "{title}" created successfully!')
                return redirect(f'wiki/{title}')
    return render(request, "encyclopedia/create.html", {"form": CreateForm()})



