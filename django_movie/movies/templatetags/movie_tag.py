from django import template
from movies.models import Category, Movie

register = template.Library()


@register.simple_tag()
def get_categories():
    """Вывод всех категорий"""

    return Category.objects.all().only("name")


@register.inclusion_tag('movies/tags/last_movie.html')
def get_last_movies(count=5):
    """Вывод последних добавленных фильмов"""

    movies = Movie.objects.filter(draft=False).order_by("id").reverse().only("title", "tagline", "poster", "url")[:count]
    return {"last_movies": movies}
