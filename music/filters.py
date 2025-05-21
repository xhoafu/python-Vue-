import django_filters
from .models import Music


class MusicFilter(django_filters.FilterSet):
    author_name = django_filters.CharFilter(field_name='author__name', lookup_expr='icontains', label='Author')
    title = django_filters.CharFilter(lookup_expr='exact',label='Music')

    class Meta:
        model = Music
        fields = ['author_name','title']

    def multi_field_filter(self, queryset, name, value):

        return queryset.filter(
            Q(title__icontains=value) | Q(name__icontains=value)
        )