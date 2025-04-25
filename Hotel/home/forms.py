from django import forms
from .models import Item, Topic

class ItemForm(forms.ModelForm):
    class Meta:
        model = Item
        fields = ['name', 'ID', 'availability', 'description', 'topic']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter item name (max 12 chars)',
                'maxlength': 12,
            }),
            'ID': forms.NumberInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter unique ID'
            }),
            'availability': forms.CheckboxInput(attrs={
                'class': 'form-check-input'
            }),
            'description': forms.Textarea(attrs={
                'class': 'form-control', 
                'rows': 4, 
                'placeholder': 'Describe the item'
            }),
            'topic': forms.Select(attrs={
                'class': 'form-select'
            }),
        }
        
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Add custom error messages
        self.fields['name'].error_messages = {
            'max_length': 'Name cannot exceed 12 characters.',
            'required': 'Item name is required.'
        }
        self.fields['ID'].error_messages = {
            'unique': 'This ID is already in use. Please provide a unique ID.',
            'required': 'Item ID is required.'
        }
        
        # Make topic queryset ordered by name
        self.fields['topic'].queryset = Topic.objects.all().order_by('name')
        self.fields['topic'].empty_label = "-- Select Category --"