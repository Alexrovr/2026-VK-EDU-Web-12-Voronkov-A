from django import template
from django.templatetags.static import static

register = template.Library()

@register.filter
def get_avatar(user):
    # Проверяем, есть ли у пользователя связь с профилем
    if hasattr(user, 'profile') and user.profile.avatar:
        return user.profile.avatar.url
    return static('img/default-avatar.png')
