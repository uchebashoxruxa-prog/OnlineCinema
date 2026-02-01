from django.contrib.auth.models import User
from django.db import models

# Create your models here.
from django.urls import reverse


class Category(models.Model):
    title = models.CharField(max_length=50, verbose_name='Название категории')

    def __str__(self):
        return self.title

    def get_absolute_url(self):  # Умная ссылка
        return reverse('category', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Категорию'
        verbose_name_plural = 'Категории'


class Actor(models.Model):
    full_name = models.CharField(max_length=150, verbose_name='ФИО актёра')
    avatar = models.ImageField(upload_to='actors', verbose_name='Фото актёра')

    def __str__(self):
        return self.full_name

    class Meta:
        verbose_name = 'Актёра'
        verbose_name_plural = 'Актёры'


class Cinema(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название фильма')
    description = models.TextField(verbose_name='Описание')
    year = models.CharField(max_length=20, verbose_name='Год выпуска')
    country = models.CharField(max_length=150, verbose_name='Страна(ы)')
    photo = models.ImageField(upload_to='photos/', verbose_name='Фото')
    video = models.FileField(upload_to='videos/', null=True, blank=True, verbose_name='Видео')
    views = models.ManyToManyField('IpVisitor', verbose_name='Просмотры', null=True, blank=True)
    category = models.ManyToManyField(Category, verbose_name='Категория')
    actors = models.ManyToManyField(Actor, verbose_name='Актёры', related_name='actors')
    released = models.CharField(max_length=50, verbose_name='Премьера')
    trailer = models.TextField(verbose_name='Ссылка трейлёра на Ютуб')
    created_at = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, null=True, blank=True, verbose_name='Дата изменения')

    def __str__(self):
        return self.title

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://xn----8sbc4aogedete1o.xn--p1ai/image/cache/no_image-600x800.png'

    def get_absolute_url(self):  # Умная ссылка
        return reverse('cinema', kwargs={'pk': self.pk})

    def count_comment(self):
        if self.comments.all():
            return self.comments.all().count()
        else:
            return 0

    def count_views(self):
        if self.views:
            return self.views.count()
        else:
            return 0

    class Meta:
        verbose_name = 'Кинофильм'
        verbose_name_plural = 'Кинофильмы'


class Comment(models.Model):
    text = models.CharField(max_length=300, verbose_name='Текст комментария')
    author = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name='Автор', related_name='comments')
    cinema = models.ForeignKey(Cinema, on_delete=models.CASCADE, verbose_name='Кинофильм', related_name='comments')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Дата добавления')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='Дата изменения')
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True,
                               related_name='sub_comments', verbose_name='Родитель комментария')

    def __str__(self):
        return f'Комметарий от {self.author.username} на кинофильм {self.cinema.title}'

    def author_photo(self):
        return self.author.profileuser.get_photo()

    class Meta:
        verbose_name = 'Комментарий'
        verbose_name_plural = 'Комментарии'


class ProfileUser(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, verbose_name='Пользователь')
    is_online = models.BooleanField(default=False, verbose_name='Статус Автоиризации')
    photo = models.ImageField(upload_to='profiles/', verbose_name='Фото', null=True, blank=True)
    about = models.CharField(max_length=200, verbose_name='Кратко о себе', null=True, blank=True)
    location = models.CharField(max_length=100, verbose_name='С какого города', null=True, blank=True)

    def __str__(self):
        return f'Профиль пользователя {self.user.username}'

    class Meta:
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'

    def get_photo(self):
        if self.photo:
            return self.photo.url
        else:
            return 'https://cdn.tlgbot.ru/i/37/97/3797f40371237023b835498b3ce757b8.jpg'

    def count_comment(self):
        if self.user.comments.all():
            return self.user.comments.all().count()
        else:
            return 0


class IpVisitor(models.Model):
    ip = models.CharField(max_length=50, verbose_name='IP посетителя')

    def __str__(self):
        return self.ip

    class Meta:
        verbose_name = 'IP посетителя'
        verbose_name_plural = 'IP посетителей'

