from rest_framework import serializers
from .models import *


class AthleteSerializaer(serializers.Model):
    class Meta:
        model = Athlete
        fields = ['id', 'name', 'sex', 'birth_year']


class GamesSerializaer(serializers.Model):
    class Meta:
        model = Games
        fields = ['games', 'season', 'year', 'city']


class EventSerializaer(serializers.Model):
    class Meta:
        model = Event
        fields = ['id', 'event', 'sport', 'gameId']


class NocSerializaer(serializers.Model):
    class Meta:
        model = Noc
        fields = ['acronym', 'region', 'notes']


class TeamSerializaer (serializers.Model):
    class Meta:
        model = Team
        fields = ['team', 'nocId']


class AthleteEventStatSerializaer(serializers.Model):
    class Meta:
        model = AthleteEventStat
        fields = ['id', 'atlheteId', 'height', 'weight',
                  'eventId', 'teamId', 'medal']
