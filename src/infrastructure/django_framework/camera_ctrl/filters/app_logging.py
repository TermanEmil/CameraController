import django_filters

from camera_ctrl.models import HistoryUnit


class LogFilter(django_filters.FilterSet):
    log_type = django_filters.CharFilter(lookup_expr='iexact')
    category = django_filters.CharFilter(lookup_expr='iexact')

    title_content = django_filters.CharFilter(lookup_expr='icontains')

    class Meta:
        model = HistoryUnit
        fields = ['log_type', 'category', 'title_content']