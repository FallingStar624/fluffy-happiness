from django.contrib import admin
from .models import Movie, MovieComment, Genre, CheckTime
from .forms import MovieCommentForm

# Register your models here.

admin.site.register(Movie)
admin.site.register(MovieComment)
admin.site.register(Genre)
admin.site.register(CheckTime)


class ReviewAdmin(admin.ModelAdmin):
    form = MovieCommentForm