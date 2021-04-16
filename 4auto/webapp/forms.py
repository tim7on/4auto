from django import forms
from webapp.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        exclude = ['owner', 'updated', 'created']
