from django import forms
from django.contrib.auth.forms import (UserCreationForm, UserChangeForm,
                                       AuthenticationForm,
                                       PasswordChangeForm)

from . import models


class AuthorForm(forms.ModelForm):

    class Meta:
        model = models.Author

        fields = ('first_name', 'last_name', 'birth_date', 'birth_place',
                  'death_date', 'death_place', 'biography', 'photo')


class BookForm(forms.ModelForm):

    class Meta:
        model = models.Book

        fields = ('title', 'release_date', 'author', 'description', 'cover')


class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment

        fields = ('text',)


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = models.CustomUser

        # fields = ('username', 'first_name', 'last_name', 'email', 'status', 'description', 'photo')
        fields = ('username', 'email')
        # fields = '__all__'


class CustomUserUpdateForm(UserChangeForm):

    class Meta:
        model = models.CustomUser

        fields = ('username', 'first_name', 'last_name', 'email', 'status', 'description', 'photo')
        # fields = '__all__'


class CustomUserLoginForm(AuthenticationForm):

    class Meta:

        fields = '__all__'


class CustomUserChangePassword(PasswordChangeForm):

    class Meta:

        fields = '__all__'