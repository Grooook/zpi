from django import template
import json
register = template.Library()


@register.filter(name='message')
def cut(value):
    json_object = json.loads(value.replace("'", '"'))
    return json_object['message']
