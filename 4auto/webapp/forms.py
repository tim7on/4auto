from django import forms
from webapp.models import Item


class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'category', 'photo',
                  'description','phone','whats','insta', 'price', 'currency']
