from django import forms
from .models import FeaturedNews

class FeaturedNewsForm(forms.ModelForm):
    class Meta:
        model = FeaturedNews
        fields = [
            'title', 'icon_image', 'grand_title', 'content', 'author', 
            'grand_image', 'cooking_time', 'calories', 'comments', 'time_added'
        ]
        widgets = {
            'time_added': forms.DateInput(format='%d/%m', attrs={'type': 'date'}),
        }