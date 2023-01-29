from django import template
from ..services import is_user_signin

register = template.Library()

@register.simple_tag()
def check_is_us_signin(username):
    return is_user_signin(username)

