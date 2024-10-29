from django import forms 
from .models import Todo 

class TodoForm(forms.ModelForm):
    class Meta:
        model = Todo 
        fields = ['title','details','priority','status','due_date','category','tags']
        widgets = {
        'title': forms.TextInput(attrs={
            'class': 'form-control', 
            'placeholder': 'Enter Task Title',
        }),
        'details':forms.Textarea(attrs={
            'class': 'form-control',
            'placeholder':'Enter Task Details',
            'rows':4,
        }),
        'priority':forms.Select(attrs={
            'class':'form-control',
        }),
        'status':forms.Select(attrs={
            'class':'form-control',
        }),
        'due_date':forms.DateInput(attrs={
            'class':'form-control',
            'type':'datetime-local',
        }),
        'tags':forms.TextInput(attrs={
            'class':'form-control',
            'placeholder':'Enter tags (comma-separated)'
        })
    }