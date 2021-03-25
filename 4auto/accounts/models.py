from django.db import models
from django.contrib.auth import get_user_model
from uuid import uuid4
from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.utils.timezone import now
from datetime import timedelta
from django.core.validators import RegexValidator
from django.utils.translation import ugettext_lazy as _
from django.urls import reverse

User._meta.get_field('email')._unique = True
User._meta.get_field('email').blank = False
User._meta.get_field('email').null = False

TOKEN_TYPE_REGISTER = 'register'
TOKEN_TYPE_PASSWORD_RESET = 'password_reset'
TOKEN_TYPE_CHOICES = (
    (TOKEN_TYPE_REGISTER, 'Регистрация'),
    (TOKEN_TYPE_PASSWORD_RESET, 'Восстановление пароля')
)


class AuthToken(models.Model):
    token = models.UUIDField(verbose_name='Токен', default=uuid4)
    user: AbstractUser = models.ForeignKey(get_user_model(), on_delete=models.CASCADE,
                                           related_name='tokens', verbose_name='Пользователь')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Создан')
    life_days = models.IntegerField(
        default=7, verbose_name='Срок действия (в днях)')
    type = models.CharField(max_length=20, choices=TOKEN_TYPE_CHOICES,
                            default=TOKEN_TYPE_REGISTER, verbose_name='Тип токена')

    @classmethod
    def get_token(cls, token):
        try:
            return cls.objects.get(token=token)
        except cls.DoesNotExist:
            return None

    def is_alive(self):
        return (self.created_at + timedelta(days=self.life_days)) >= now()

    def __str__(self):
        return self.user.username

    class Meta:
        verbose_name = 'Аутентификационный токен'
        verbose_name_plural = 'Аутентификационные токены'


class Profile(models.Model):
    phone_regex = RegexValidator(
        regex=r'^\+?1?\d{12,15}$', message="Телефон должен быть в формате: '+996XXXXXXXXX'.")
    insta_regex = RegexValidator(
        regex=r'([A-Za-z0-9_](?:(?:[A-Za-z0-9_]|(?:\.(?!\.))){0,28}(?:[A-Za-z0-9_]))?)'
    )

    user: AbstractUser = models.OneToOneField(get_user_model(), related_name='profile',
                                              on_delete=models.CASCADE, verbose_name='Пользователь')

    adress = models.CharField(
        max_length=50, verbose_name=_("Адрес"), null=True, blank=True)
    schedule = models.CharField(max_length=50, verbose_name=_(
        "Расписание"), null=True, blank=True)
    avatar = models.ImageField(
        null=True, blank=True, upload_to='user_pics', verbose_name=_("Аватар"))
    phone = models.CharField(
        validators=[phone_regex], verbose_name="Телефон", max_length=16, blank=True, null=True)
    whats = models.CharField(
        validators=[phone_regex], verbose_name="Whatsapp", max_length=16, blank=True, null=True)
    insta = models.CharField(
        validators=[insta_regex], verbose_name="Instagram", max_length=31, blank=True, null=True)

    def __str__(self):
        return self.user.username + "Профиль"

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_absolute_url(self):
        return reverse('profile', kwargs={'username': self.user.username})
