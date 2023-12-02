import django_filters
from .models import Planta

class PlantaFilter(django_filters.FilterSet):
    nome = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = Planta
        fields = ['nome']