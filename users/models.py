from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    username = None
    email = models.EmailField(unique=True, verbose_name='Email')
    
    avatar = models.ImageField(upload_to='users/avatars', blank=True, null=True, verbose_name='Аватар',
                               help_text='Загрузите аватар')
    phone_number = models.CharField(max_length=35, verbose_name='Номер телефона', blank=True, null=True,
                                    help_text='Введите номер телефона')
    side = models.CharField(max_length=35, verbose_name='Страна', blank=True, null=True, help_text='Укажите страну')
    token = models.CharField(max_length=100, verbose_name='Token', blank=True, null=True)
    
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []
    
    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'
        
    def __str__(self):
        return self.email
    