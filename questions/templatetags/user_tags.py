from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter
def get_avatar(user):
    if hasattr(user, 'profile'):
        return user.profile.get_avatar()
    return static('img/default-avatar.png')
