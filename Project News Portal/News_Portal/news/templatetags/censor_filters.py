from django import template
import re

register = template.Library()


@register.filter(name='censor')
def censor(value, unwanted_words):
    # Проходимся по каждому нежелательному слову и заменяем его на '*'
    unwanted_words = unwanted_words.split(',')
    for word in unwanted_words:
        pattern = fr'\b{re.escape(word)}\b'
        value = re.sub(pattern, '*' * len(word), value, flags=re.IGNORECASE)
    return value
