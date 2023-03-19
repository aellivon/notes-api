from django.contrib.auth import get_user_model
from rest_framework import mixins, viewsets, filters

from .serializers import UserSerializer, DivisionSerializer
from .models import Division


class UserViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = get_user_model().objects.all()
    serializer_class = UserSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'first_name', 'last_name', 'email', 'furigana_fname', 'furigana_lname',
        'position', "id"
    ]


class DivisionViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    queryset = Division.objects.all()
    serializer_class = DivisionSerializer
    filter_backends = [filters.SearchFilter]
    search_fields = [
        'name', "id"
    ]
