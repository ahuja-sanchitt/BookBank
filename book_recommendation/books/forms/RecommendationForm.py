from django import forms
from ..models import Recommendation

class RecommendationForm(forms.ModelForm):
    class Meta:
        model = Recommendation
        fields = ['bookname', 'rating', 'recommendation_text']
        widgets = {
            'bookname': forms.TextInput(attrs={'class': 'form-control'}),
            'rating': forms.NumberInput(attrs={'class': 'form-control'}),
            'recommendation_text': forms.Textarea(attrs={'class': 'form-control'}),
        }
       
