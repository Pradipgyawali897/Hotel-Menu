from django import forms
from .models import Item

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'ID', 'availability', 'description', 'topic']
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control'}),
            'ID': forms.NumberInput(attrs={'class': 'form-control'}),
            'availability': forms.CheckboxInput(attrs={'class': 'form-check-input'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'rows': 4}),
            'topic': forms.Select(attrs={'class': 'form-select'}),
        }