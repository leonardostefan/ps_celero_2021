from rest_framework import serializers
from .models import *


class AthleteSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Athlete
        fields = ['id', 'name', 'sex', 'birth_year']


class GamesSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Games
        fields = ['games', 'season', 'year', 'city']


class EventSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['id', 'event', 'sport', 'gameId']


class NocSerializaer(serializers.ModelSerializer):
    class Meta:
        model = Noc
        fields = ['acronym', 'region', 'notes']

class AthleteEventStatSerializaer(serializers.ModelSerializer):
    class Meta:
        model = AthleteEventStat
        fields = ['id', 'atlheteId', 'height', 'weight',
                  'eventId', 'team', 'medal']
