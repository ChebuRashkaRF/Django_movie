from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Movie, Category, Actor, Rating
from .forms import ReviewForm, RatingForm
from .service import GenreYear, get_client_ip


class MoviesView(GenreYear, ListView):
    """Список фильмов"""

    model = Movie
    queryset = Movie.objects.filter(draft=False).only("title", "tagline", "poster", "url")
    paginate_by = 3


class MovieDetailView(GenreYear, DetailView):
    """Полное описание фильма"""

    model = Movie
    slug_field = "url"

    def get_queryset(self, **kwargs):
        return Movie.objects.prefetch_related('actors', 'directors', 'genres')

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        try:
            rating = Rating.objects.get(
                movie__url=self.kwargs['slug'],
                ip=get_client_ip(self.request)
            )
            rating_star = str(rating.star.value)
        except Rating.DoesNotExist:
            rating = False
        if rating:
            context["star_form"] = RatingForm(instance=rating)
            context["rating_srar"] = rating_star
        else:
            context["star_form"] = RatingForm()
        context["form"] = ReviewForm()
        return context


class AddReview(View):
    """Отзывы"""

    def post(self, request, pk):
        form = ReviewForm(request.POST)
        movie = Movie.objects.get(id=pk)
        if form.is_valid():
            form = form.save(commit=False)
            if request.POST.get("parent", None):
                form.parent_id = int(request.POST.get("parent"))
            form.movie = movie
            form.save()
        return redirect(movie.get_absolute_url())


class ActorView(GenreYear, DetailView):
    """Вывод информации об актере"""

    model = Actor
    template_name = 'movies/actor.html'
    slug_field = "name_en"


class FilterMoviesView(GenreYear, ListView):
    """Фильтр фильмов"""

    paginate_by = 2

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct()
        return queryset

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["year"] = ''.join(
            [f"year={x}&" for x in self.request.GET.getlist("year")]
        )
        context["genre"] = ''.join(
            [f"genre={x}&" for x in self.request.GET.getlist("genre")]
        )
        return context


class JsonFilterMoviesView(ListView):
    """Фильтр фильмов в json"""

    def get_queryset(self):
        queryset = Movie.objects.filter(
            Q(year__in=self.request.GET.getlist("year")) |
            Q(genres__in=self.request.GET.getlist("genre"))
        ).distinct().values("title", "tagline", "url", "poster")
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = list(self.get_queryset())
        return JsonResponse({"movies": queryset}, safe=False)


class AddStarRating(View):
    """Добавление рейтинга фильму"""

    def post(self, request):
        form = RatingForm(request.POST)
        if form.is_valid():
            Rating.objects.update_or_create(
                ip=get_client_ip(request),
                movie_id=int(request.POST.get("movie")),
                defaults={'star_id': int(request.POST.get("star"))}
            )
            return HttpResponse(status=201)
        else:
            return HttpResponse(status=400)


class Search(ListView):
    """Поиск фильмов"""

    paginate_by = 1

    def get_queryset(self):
        return Movie.objects.filter(title__icontains=self.request.GET.get("q"))

    def get_context_data(self, *args, **kwargs):
        context = super().get_context_data(*args, **kwargs)
        context["q"] = f'q={self.request.GET.get("q")}&'
        return context
