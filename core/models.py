from django.db import models
from django.templatetags.static import static
from django.contrib.auth.models import User

class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile', verbose_name='Пользователь')
    avatar = models.ImageField(upload_to='avatars/%Y/%m/%d/', null=True, blank=True, verbose_name='Аватар')
    bio = models.TextField(max_length=500, null=True, blank=True, verbose_name='О себе')

    def get_avatar(self):
        if self.avatar:
            return self.avatar.url
        return static('img/default-avatar.png')

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def __str__(self):
        return f"Профиль пользователя #{self.user_id}"
