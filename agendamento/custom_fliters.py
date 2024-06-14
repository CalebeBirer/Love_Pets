from django import template

register = template.Library()

@register.filter
def status_label(finalizado):
    return 'Finalizado' if finalizado else 'Pendente'
