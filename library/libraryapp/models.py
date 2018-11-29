from django.db import models
# from django.contrib.auth.models import User
from django.contrib.auth.models import AbstractUser
from django.conf import settings

class CustomUser(AbstractUser):
    status = models.CharField(max_length=256, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    photo = models.ImageField(upload_to='users', blank=True, null=True)

    def __str__(self):
        return self.username

class Author(models.Model):
    first_name = models.CharField(max_length=256, blank=False, null=False)
    last_name = models.CharField(max_length=256, blank=False, null=False)
    biography = models.TextField(blank=True, null=True)
    birth_date = models.DateField(blank=True, null=True)
    death_date = models.DateField(blank=True, null=True)
    birth_place = models.CharField(max_length=256, blank=True, null=True)
    death_place = models.CharField(max_length=256, blank=True, null=True)
    photo = models.ImageField(upload_to='authors', blank=True, null=True)

    def __str__(self):
        return str(self.first_name) + ' ' + str(self.last_name)

class Book(models.Model):
    title = models.CharField(max_length=256, blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    release_date = models.DateField(blank=True, null=True)
    # raiting = models.FloatField(blank=True, null=False, default=0)
    cover = models.ImageField(upload_to='books', blank=True, null=True)
    author = models.ForeignKey(Author, on_delete=models.SET_NULL, blank=False, null=True)
    reader = models.ManyToManyField(settings.AUTH_USER_MODEL, blank=True)

    def __str__(self):
        return self.title

class Comment(models.Model):
    text = models.TextField(blank=False, null=False)
    date = models.DateTimeField(auto_now_add=True, blank=True, null=False)
    parent_comment = models.ForeignKey('self', on_delete=models.CASCADE, blank=True, null=True)
    book = models.ForeignKey(Book, on_delete=models.CASCADE, blank=True, null=False)
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, blank=True, null=False)

    def __str__(self):
        return self.text
