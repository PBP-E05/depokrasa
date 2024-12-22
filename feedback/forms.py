from django.utils.html import strip_tags
from django.forms import ModelForm
from feedback.models import Feedback
from django import forms
from .models import Feedback

class FeedbackForm(ModelForm):
    class Meta:
        model = Feedback
        fields = ['subject', 'message']
        widgets = {
            'subject': forms.TextInput(attrs={
                'placeholder': 'Subject',
                'class': 'form-control'
            }),
            'message': forms.Textarea(attrs={
                'placeholder': 'Write your feedback here...',
                'class': 'form-control',
                'rows': 4
            }),
        }