from django.contrib.auth.models import User, Group
from rest_framework import viewsets, permissions
from ps_celero.quickstart.serializers import UserSerializer, GruopSerializer


class UserViewSet(viewsets.ModelViewSet):
    '''
    API ENDPOIT
    '''
    queryset = User.objects.all().order_by('-date_joined')
    serializers_class = UserSerializer
    permissions = [permissions.IsAuthenticated]
