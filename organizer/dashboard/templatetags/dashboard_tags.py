from django import template
from django.utils.safestring import mark_safe

import markdown


register = template.Library()

# TODO check XSS security issue

@register.filter(name="markdown")
def markdown_format(text):
    return mark_safe(markdown.markdown(
        text,
        safe_mode='escape',
        extensions=[
            'markdown.extensions.nl2br',
            'markdown.extensions.fenced_code'
        ]
    ))
