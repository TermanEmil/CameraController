from django import template
from django.http import QueryDict

register = template.Library()


def _build_query_link(query):
    if query == '':
        return ''

    return '?' + query


@register.simple_tag(takes_context=True)
def url_var(context, name, value):
    query: QueryDict = context['request'].GET.copy()
    query[name] = value
    return _build_query_link(query.urlencode())


@register.simple_tag(takes_context=True)
def toggle_url_var(context, name, value):
    query: QueryDict = context['request'].GET.copy()

    if name in query and query[name] == value:
        query.pop(name)
    else:
        query[name] = value

    query.pop('page', None)
    return _build_query_link(query.urlencode())