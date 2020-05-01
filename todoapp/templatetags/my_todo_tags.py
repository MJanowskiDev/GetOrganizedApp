import markdown
from django import template
from django.utils.safestring import mark_safe

register = template.Library()

@register.filter(name='my_markdown')
def markdown_format(text):
    return mark_safe(markdown.markdown(text))