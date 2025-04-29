import random
import markdown2

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import NewPageForm, EditPageForm
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query_value = request.GET.get("q")
    entries = util.list_entries()
    similar_entries = []
    for entry in entries:
        if (entry.lower() == query_value.lower()):
            return redirect('entry', entry=query_value)
        else:
            if (query_value.lower() in entry.lower()):
                similar_entries.append(entry)
    return render(request, "encyclopedia/search.html", { 'similar_entries': similar_entries })

def create_page(request):
    if request.method == 'POST':
        form = NewPageForm(request.POST)
        if form.is_valid():
            page_title = form.cleaned_data["page_title"]
            page_content = form.cleaned_data["page_content"]
            # Check if name already exists
            entries = util.list_entries()
            for entry in entries:
                if (entry.lower() == page_title.lower()):
                    return render(request, "encyclopedia/error.html", {
                        "title": f'Error creating "{entry}" page',
                        "message": f'The entry "{entry}" has already been created, please try a different one.'
                    })
            # prepend the title in the markdown fle
            util.save_entry(page_title, f"#{page_title}\n{page_content}")
            return redirect('entry', entry=page_title)
        else:
            return render(request, "encyclopedia/create-page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create-page.html", {
            "form": NewPageForm
        })
    
def edit_page(request, entry):
    if request.method == 'POST':
        form = EditPageForm(request.POST)
        if form.is_valid():
            page_content = form.cleaned_data["page_content"]
            # prevent title from being changed
            util.save_entry(entry, f"#{entry}\n{page_content}")
            return redirect('entry', entry=entry)
        else:
            return render(request, "encyclopedia/edit-page.html", {
                "entry": entry,
                "form": form
            })
    else:
        entry_content = util.get_entry(entry)
        entry_without_title = entry_content.split("\n", 1)[1].strip()
        form = EditPageForm(initial={'page_content': entry_without_title})
        return render(request, "encyclopedia/edit-page.html", {
            "entry": entry,
            "entry_content": entry_without_title,
            "form": form
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', entry=random_entry)

def entry(request, entry):
    try:
        html_text = markdown2.markdown(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "entry_name": entry,
            "entry": html_text
        })
    except:
        return render(request, "encyclopedia/not-found.html")