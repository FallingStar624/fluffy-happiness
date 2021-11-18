from django import forms
from .models import Review, ReviewComment
from .widgets import AutoCompleteWidget, starWidget

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'movie_title', 'rank', 'content']
        widgets = {
            'grade': starWidget,
        }


class ReviewCommentForm(forms.ModelForm):

    class Meta:
        model = ReviewComment
        exclude = ['review', 'user']