import django_filters
from django_filters import CharFilter
from .models import *

class ProductFilter(django_filters.FilterSet):
    name = django_filters.CharFilter(label='Key-Word',lookup_expr='icontains')
    price = django_filters.NumberFilter(label='Price',field_name="price", lookup_expr='lte')
    class Meta:
        model = Product
        fields = ['name','price', 'tags']