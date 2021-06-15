
import json
from typing import Tuple

from .serializers import *
from .models import Athlete
from rest_framework.decorators import api_view
from rest_framework import status

from django.core.exceptions import ObjectDoesNotExist
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt


# ------------------------------------
# Referente aos Atletas
@api_view(["GET"])
@csrf_exempt
def getAthleteByName(request):
    '''
    Realiza consulta de Athleta pelo campo 'nome' informado em query
    '''
    if 'name' in request.GET:
        # if name:
        name = request.GET["name"]
        athlete = Athlete.objects.filter(name=name)[0]
        serializer = AthleteSerializaer(athlete, many=False)
        r = serializer.data
    else:
        r = 'empty'

    return JsonResponse(r, safe=False, status=status.HTTP_200_OK)


def getAthleteById(request, id):
    '''
    Realiza consulta de Athleta pelo 'id' informado em query
    '''
    athlete = Athlete.objects.get(id=id)
    serializer = AthleteSerializaer(athlete, many=False)
    r = serializer.data

    return JsonResponse(r, safe=False, status=status.HTTP_200_OK)


@api_view(["GET"])
@csrf_exempt
def getAthletes(request):
    '''
    Retorna a lista completa de atletas.
    '''
    athlete = Athlete.objects.filter()
    serializer = AthleteSerializaer(athlete, many=True)
    r = serializer.data
    return JsonResponse(r, safe=False, status=status.HTTP_200_OK)


@api_view(["PUT"])
@csrf_exempt
def updateAthlete(request, id):
    '''
    Altera informações de atlheta especifico
    '''
    print(request.body)

    payload = json.loads(request.body)
    try:
        athlete_item = Athlete.objects.filter(id=id)
        
        athlete_item.update(**payload)
        athlete = Athlete.objects.get(id=id)
        serializer = AthleteSerializaer(athlete)
        r = serializer.data
        return JsonResponse({'athlete': r}, safe=False, status=status.HTTP_202_ACCEPTED)

    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Algo inesperado aconteceu'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["POST"])
@csrf_exempt
def createAthletes(request):
    '''
    Insere um novo atleta na base de dados
    '''
    payload = json.loads(request.body)
    try:
        athlete = Athlete.objects.create(**payload)
        serializer = AthleteSerializaer(athlete)
        r = serializer.data
        return JsonResponse({'athlete': r}, safe=False, status=status.HTTP_201_CREATED)
    except Exception:
        return JsonResponse({'error': 'Algo inesperado aconteceu'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


@api_view(["DELETE"])
@csrf_exempt
def deleteAtlhete(request, id):
    '''
    Remove informações de atleta especifico
    '''
    try:
        athlete = Athlete.objects.get(id=id)
        athlete.delete()
        return JsonResponse(status=status.HTTP_202_ACCEPTED)
    except ObjectDoesNotExist as e:
        return JsonResponse({'error': str(e)}, safe=False, status=status.HTTP_404_NOT_FOUND)
    except Exception:
        return JsonResponse({'error': 'Ocorreu algum erro'}, safe=False, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


# ------------------------------------
# Referente aos eventos
@ api_view(["GET"])
@ csrf_exempt
def getEvents(request):
    event = Event.objects.all
    serializer = EventSerializaer(event, many=True)
    return JsonResponse({'events': serializer.data}, safe=False, status=status.HTTP_200_OK)


@ api_view(["GET"])
@ csrf_exempt
def getAthleteEventById(request,id):
    athleteevent = AthleteEventStat.objects.get(id=id)
    serializer = AthleteEventStatSerializaer(athleteevent, many=False)
    result = serializer.data
    if 'full_tree'  in request.GET:
        event = Event.objects.get(event=athleteevent.event)
        game = Games.objects.get(game =event.gameId)
        athlete = Athlete.objects.get(id=athleteevent.atlheteId)
        noc = Noc.objects.get(acronym=athleteevent.noc)
        pass
    
    


    return JsonResponse({'events': serializer.data}, safe=False, status=status.HTTP_200_OK)





# ------------------------------------
# Referente aos jogos
@ api_view(["GET"])
@ csrf_exempt
def getGames(request):
    games = Games.objects.filter(name=request.data.name)
    serializer = GamesSerializaer(games, many=True)
    return JsonResponse({'games_list': serializer.data}, safe=False, status=status.HTTP_200_OK)


# ------------------------------------
# Referente aos eventos
@ api_view(["GET"])
@ csrf_exempt
def getAthlete(request):
    athlete = Athlete.objects.filter(name=request.data.name)
    serializer = AthleteSerializaer(athlete, many=True)
    return JsonResponse({'athletes': serializer.data}, safe=False, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @csrf_exempt
# def getAthlete(request):
#     athlete = Athlete.objects.filter(name=request.data.name)
#     serializer = AthleteSerializaer(athlete, many=True)
#     return JsonResponse({'athletes': serializer.data}, safe=False, status=status.HTTP_200_OK)


# @api_view(["GET"])
# @csrf_exempt
# def getAthlete(request):
#     athlete = Athlete.objects.filter(name=request.data.name)
#     serializer = AthleteSerializaer(athlete, many=True)
#     return JsonResponse({'athletes': serializer.data}, safe=False, status=status.HTTP_200_OK)
