from django import template
from ..services import is_user_signin, get_categories_query

register = template.Library()

@register.simple_tag()
def check_is_us_signin(username):
    return is_user_signin(username)

@register.simple_tag()
def get_categories_list():
    return get_categories_query()