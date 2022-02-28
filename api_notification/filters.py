import django_filters

from .models import MallingList


class MallingListFilter(django_filters.FilterSet):
    tag = django_filters.CharFilter(
        method='tag_filter',
        label='Тег'
    )
    code = django_filters.CharFilter(
        method='code_filter',
        label='Код оператора'
    )

    class Meta:
        model = MallingList
        fields = ('tag', 'code')

    def tag_filter(self, queryset, name, value):
        if value:
            return queryset.prefetch_related(
                'messages__client__tag'
            ).filter(
                messages__client__tag_id__name=value
            )
        return queryset

    def code_filter(self, queryset, name, value):
        if value:
            return queryset.prefetch_related(
                'messages__client__mobile_operator_code'
            ).filter(
                messages__client__mobile_operator_code__code=value
            )
        return queryset
