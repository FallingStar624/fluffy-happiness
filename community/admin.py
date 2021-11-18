from django.contrib import admin
from .models import Review, ReviewComment
from .forms import ReviewForm

# Register your models here.

admin.site.register(Review)
admin.site.register(ReviewComment)


class ReviewAdmin(admin.ModelAdmin):
    form = ReviewForm