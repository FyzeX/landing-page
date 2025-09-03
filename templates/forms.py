from django import forms
from .models import Review


class ReviewForm(forms.ModelForm):
    """
    Form for creating template reviews
    """
    class Meta:
        model = Review
        fields = ['rating', 'comment']
        widgets = {
            'rating': forms.Select(
                choices=[(i, f'{i} Star{"s" if i != 1 else ""}') for i in range(1, 6)],
                attrs={'class': 'form-select'}
            ),
            'comment': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Share your experience with this template...'
            })
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['rating'].empty_label = None
        self.fields['comment'].required = False