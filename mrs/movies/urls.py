from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns
from movies import views

urlpatterns = [
    path('city/', views.CityList.as_view()),
    path('theater/', views.TheaterList.as_view()),
    path('theaterseat/', views.TheaterSeatList.as_view()),
    path('movie/', views.MovieList.as_view()),
    path('show/', views.ShowList.as_view()),

    # path('snippets/<int:pk>/', views.SnippetDetail.as_view()),
]

urlpatterns = format_suffix_patterns(urlpatterns)
