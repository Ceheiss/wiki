from django import forms

class NewPageForm(forms.Form):
    page_title = forms.CharField(label='title')
    page_content = forms.CharField(widget=forms.Textarea, label='content')

