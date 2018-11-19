from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView)
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render

from . import models, forms


class AboutView(TemplateView):
    template_name = 'libraryapp/about.html'

#############################################################
# book block
class BookListView(ListView):
    model = models.Book
    # template_name = 'libraryapp/book_list.html'

    paginate_by = 15
    ordering = ['-release_date']

    def get_queryset(self):
        return models.Book.objects.all()

class BookDetailView(DetailView):
    model = models.Book
    template_name = 'libraryapp/book_detail.html'

class BookCreateView(CreateView, LoginRequiredMixin):
    model = models.Book
    # template_name = 'libraryapp/book_create.html'

    login_url = '/login/'
    success_url = 'libraryapp/book_detail.html'

    form_class = forms.BookForm

class BookUpdateView(UpdateView, LoginRequiredMixin):
    models = models.Book
    # template_name = 'libraryapp/book_create.html'

    login_url = '/login/'
    success_url = 'libraryapp/book_detail.html'

    form_class = forms.BookForm

#############################################################
# author block
class AuthorListView(ListView):
    model = models.Author
    # template_name = 'libraryapp/author_list.html'

    paginate_by = 15
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        return models.Author.objects.all()

class AuthorDetailView(DetailView):
    model = models.Author
    # template_name = 'libraryapp/author_detail.html'

class AuthorCreateView(CreateView, LoginRequiredMixin):
    model = models.Author
    # template_name = 'libraryapp/author_create.html'

    login_url = '/login/'
    success_url = 'libraryapp/author_detail.html'

    form_class = forms.AuthorForm

class AuthorUpdateView(UpdateView, LoginRequiredMixin):
    model = models.Author
    # template_name = 'libraryapp/author_create.html'

    login_url = '/login/'
    # redirect_field_name = 'libraryapp/author_detail.html'
    success_url = 'libraryapp/author_detail.html'

    form_class = forms.AuthorForm

#############################################################
# user block

class UserCreateView(CreateView):
    model = 'auth.User'

    success_url = 'registration/user_detail.html'
    template_name = 'registration/signup.html'

    form_class = UserCreationForm

class UserUpdateView(UpdateView):
    model = 'auth.User'
    template_name = 'registration/user_detail.html'

    success_url = 'registration/user_detail.html'

    form_class = UserCreationForm

############################################################

@login_required
def add_comment_to_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)

    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.book = book
            comment.save()
            return redirect('post_detail', pk=book.pk)
    else:
        form = forms.CommentForm()
    return render(request, 'libraryapp/comment_form.html', {'form': form})

@login_required
def remove_comment(request, pk):
    comment = get_object_or_404(models.Comment, pk=pk)
    book_pk = comment.book.pk
    comment.delete()
    return redirect('book_detail', pk=book_pk)
