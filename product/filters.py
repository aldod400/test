import django_filters

from .models import Product

class ProductFilter(django_filters.FilterSet):
    filter = django_filters.CharFilter(lookup_expr="iexact")
    name = django_filters.CharFilter(field_name='name', lookup_expr='icontains')
    minPrice = django_filters.NumberFilter(field_name='price', lookup_expr='gte')
    maxPrice = django_filters.NumberFilter(field_name='price', lookup_expr='lte')
    class Meta:
        model = Product
        fields = ('category', 'brand', 'name', 'minPrice', 'maxPrice')