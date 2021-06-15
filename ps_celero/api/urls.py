from django.urls import include, path
from . import views

urlpatterns = [
    path(r'athlete', views.getAthleteByName),
    path(r'athlete/<int:id>', views.getAthleteById),
    path(r'athlete_list', views.getAthletes),
    path(r'athlete/update/<int:id>', views.updateAthlete),
    path(r'athlete/create', views.createAthletes),
    path(r'athlete/delete/<int:id>', views.deleteAtlhete),


    path(r'event_list', views.getEvents),


    path(r'athlet_event/<int:id>', views.getAthleteEventById),



    path(r'games_list', views.getGames),



    path(r'athlete_list', views.getAthletes),

    path(r'athlete_list', views.getAthletes),

    path(r'athlete_list', views.getAthletes),

]
