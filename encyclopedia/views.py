import random
import markdown2

from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from .forms import NewPageForm
from . import util

def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })

def search(request):
    query_value = request.GET.get("q")
    entries = util.list_entries()
    print("all entries", entries)
    print("Check the request: ", query_value)
    similar_entries = []
    for entry in entries:
        print("entrada", entry)
        if (entry.lower() == query_value.lower()):
            return redirect('entry', entry=query_value)
        else:
            if (query_value.lower() in entry.lower()):
                similar_entries.append(entry)
        print(similar_entries)
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
            return HttpResponseRedirect('/')
        else:
            return render(request, "encyclopedia/create-page.html", {
                "form": form
            })
    else:
        return render(request, "encyclopedia/create-page.html", {
            "form": NewPageForm
        })

def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)
    return redirect('entry', entry=random_entry)

def entry(request, entry):
    print("check request:", request, entry)
    try:
        html_text = markdown2.markdown(util.get_entry(entry))
        return render(request, "encyclopedia/entry.html", {
            "entry": html_text
        })
    except:
        return render(request, "encyclopedia/not-found.html")