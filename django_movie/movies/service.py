from .models import Movie, Genre


class GenreYear:
    """Жанры и года выхода фильмов"""

    def get_genres(self):
        return Genre.objects.only("name")

    def get_years(self):
        return Movie.objects.filter(draft=False).values("year")


def get_client_ip(request):
    """Возвращает ip текущего пользователя"""

    x_forwarded_for = request.META.get('HTTP_X_FORWARDED_FOR')
    if x_forwarded_for:
        ip = x_forwarded_for.split(',')[0]
    else:
        ip = request.META.get('REMOTE_ADDR')
    return ip
