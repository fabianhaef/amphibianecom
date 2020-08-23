import django_filters
from .models import *
from taggit.forms import TagField


class ProductFilter(django_filters.FilterSet):
    class Meta:
        model = Product
        fields = ['title']


class TagFilter(django_filters.CharFilter):
    field_class = TagField

    def __init__(self, *args, **kwargs):
        kwargs.setdefault('lookup_expr', 'in')
        super().__init__(*args, **kwargs)


class MyTagFilter(django_filters.FilterSet):
    tags = TagFilter(field_name='tags__name')

    class Meta:
        model = Product
        fields = ['tags']
