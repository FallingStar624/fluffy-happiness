from django import forms
from .models import Review, ReviewComment

class ReviewForm(forms.ModelForm):

    class Meta:
        model = Review
        fields = ['title', 'movie_title', 'rank', 'content']


class ReviewCommentForm(forms.ModelForm):

    class Meta:
        model = ReviewComment
        exclude = ['review', 'user']