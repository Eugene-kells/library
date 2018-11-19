from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView)
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render
from django.urls import reverse_lazy

from . import models, forms

#############################################################
# about this site view block
class AboutView(TemplateView):
    template_name = 'libraryapp/about.html'


#############################################################
# book block
class BookListView(ListView):
    model = models.Book
    template_name = 'libraryapp/book_list.html'

    paginate_by = 15
    ordering = ['-release_date']

    def get_queryset(self):
        return models.Book.objects.all()


class BookDetailView(DetailView):
    model = models.Book
    template_name = 'libraryapp/book_detail.html'


class BookCreateView(CreateView, LoginRequiredMixin):
    model = models.Book
    form_class = forms.BookForm

    template_name = 'libraryapp/book_create.html'

    login_url = '/login/'
    # success_url = 'libraryapp/book_detail.html'
    success_url = reverse_lazy('book_detail', kwargs={'pk': model.pk})

    def form_valid(self, form):
        book = form.save()
        return reverse_lazy('libraryapp:book_detail', kwargs={'pk': book.pk})


class BookUpdateView(UpdateView, LoginRequiredMixin):
    models = models.Book
    form_class = forms.BookForm
    template_name = 'libraryapp/book_update.html'

    login_url = '/login/'
    # success_url = 'libraryapp/book_detail.html'

    def form_valid(self, form):
        book = form.save()
        return reverse_lazy('libraryapp:book_detail', kwargs={'pk': book.pk})


#############################################################
# author block
class AuthorListView(ListView):
    model = models.Author
    template_name = 'libraryapp/author_list.html'

    paginate_by = 15
    ordering = ['last_name', 'first_name']

    def get_queryset(self):
        return models.Author.objects.all()


class AuthorDetailView(DetailView):
    model = models.Author
    template_name = 'libraryapp/author_detail.html'


class AuthorCreateView(CreateView, LoginRequiredMixin):
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'libraryapp/author_create.html'

    login_url = '/login/'
    # success_url = 'libraryapp/author_detail.html'

    def form_valid(self, form):
        author = form.save()
        return reverse_lazy('libraryapp:author_detail', kwargs={'pk': author.pk})


class AuthorUpdateView(UpdateView, LoginRequiredMixin):
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'libraryapp/author_update.html'

    login_url = '/login/'
    # redirect_field_name = 'libraryapp/author_detail.html'
    # success_url = 'libraryapp/author_detail.html'

    def form_valid(self, form):
        author = form.save()
        return reverse_lazy('libraryapp:author_detail', kwargs={'pk': author.pk})


#############################################################
# user block

class UserCreateView(CreateView):
    model = models.CustomUser
    form_class = forms.CustomUserCreationForm
    template_name = 'registration/signup.html'

    # success_url = 'registration/user_detail.html'

    def form_valid(self, form):
        user = form.save()
        return reverse_lazy('libraryapp:user', kwargs={'pk': user.pk})


class UserUpdateView(UpdateView):
    model = models.CustomUser
    form_class = forms.CustomUserUpdateForm
    template_name = 'registration/user_detail.html'

    # success_url = 'registration/user_detail.html'

    def form_valid(self, form):
        user = form.save()
        return reverse_lazy('libraryapp:user', kwargs={'pk': user.pk})


class UserDetailView(DetailView):
    model = models.CustomUser
    template_name = 'registration/user_detail.html'


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
