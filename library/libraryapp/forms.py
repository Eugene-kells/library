from django import forms

from . import models


class AuthorForm(forms.ModelForm):

    class Meta:
        model = models.Author

        fields = ('first_name', 'last_name', 'birth_date', 'biography', 'photo')

        widgets = {
            'first_name': forms.TextInput(attrs={'class': 'authorinputclass'}),
            'last_name': forms.TextInput(attrs={'class': 'authorinputclass'}),
            # 'birth_date': forms.DateField()
            'biography': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
            # 'photo': forms.ImageField(),
        }

class BookForm(forms.ModelForm):

    class Meta:
        model = models.Book

        fields = ('title', 'release_date', 'author', 'description', 'cover')

        widgets = {
            'title': forms.TextInput(attrs={'class': 'bookinputclass'}),
            'description': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }

class CommentForm(forms.ModelForm):

    class Meta:
        model = models.Comment

        fields = ('text',)

        widgets = {
            'text': forms.Textarea(attrs={'class': 'editable medium-editor-textarea postcontent'}),
        }