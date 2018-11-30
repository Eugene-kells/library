from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView)
from django.shortcuts import get_object_or_404, redirect
from django.shortcuts import render, render_to_response
from django.urls import reverse_lazy
from django.contrib.auth.views import LoginView, PasswordChangeView
from django.template import RequestContext

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


class BookCreateView(LoginRequiredMixin, CreateView):
    model = models.Book
    form_class = forms.BookForm

    template_name = 'libraryapp/book_create.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        book = form.save() # here is some problem
        return super(BookCreateView, self).form_valid(form)


class BookUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Book
    form_class = forms.BookForm
    template_name = 'libraryapp/book_update.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        book = form.save() # here is some problem
        return super(BookUpdateView, self).form_valid(form)


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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = models.Book.objects.filter(author=self.object.pk).values()
        return context


class AuthorCreateView(LoginRequiredMixin, CreateView):
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'libraryapp/author_create.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        author = form.save() # here is some problem
        return super(AuthorCreateView, self).form_valid(form)


class AuthorUpdateView(LoginRequiredMixin, UpdateView):
    model = models.Author
    form_class = forms.AuthorForm
    template_name = 'libraryapp/author_update.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('author_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        author = form.save() # here is some problem
        return super(AuthorUpdateView, self).form_valid(form)


#############################################################
# user authentication block

class UserCreateView(CreateView):
    model = models.CustomUser
    form_class = forms.CustomUserCreationForm
    template_name = 'registration/signup.html'

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        user = form.save()
        return super(UserCreateView, self).form_valid(form)


class UserUpdateView(LoginRequiredMixin, UserPassesTestMixin, UpdateView):
    model = models.CustomUser
    form_class = forms.CustomUserUpdateForm
    template_name = 'registration/user_update.html'

    login_url = '/login/'


    def get_success_url(self):
        return reverse_lazy('user', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        user = form.save() # here is some problem
        return super(UserUpdateView, self).form_valid(form)

    # check if this user is owner of the form they want to access
    def test_func(self):
        return self.kwargs['pk'] == self.request.user.pk


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.CustomUser
    template_name = 'registration/user_detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all
        return context



class UserLoginView(LoginView):
    form_class =forms.CustomUserLoginForm
    template_name = 'registration/login.html'



class UserChangePasswordView(LoginRequiredMixin, UserPassesTestMixin, PasswordChangeView):
    form_class = forms.CustomUserChangePassword
    template_name = 'registration/change_password.html'

    login_url = '/login/'


    def get_success_url(self):
        return reverse_lazy('about')

    def form_valid(self, form):
        user = form.save()
        return super(UserChangePasswordView, self).form_valid(form)

    # check if this user is owner of the form they want to access
    def test_func(self):
        return self.kwargs['pk'] == self.request.user.pk


############################################################
# default error pages block

# def error_400(request, exception):
def error_400(request): # TODO :: change it back
    context = RequestContext(request)
    err_code = 400
    response = render(request, 'errors/error_400.html', {'code': err_code}, context)
    response.status_code = 400
    return response
    # return render(request, 'errors/error_404.html')

# def error_403(request, exception):
def error_403(request): # TODO :: change it back
    context = RequestContext(request)
    err_code = 403
    response = render(request, 'errors/error_403.html', {'code': err_code}, context)
    response.status_code = 403
    return response
    # return render(request, 'errors/error_404.html')

# def error_404(request, exception):
def error_404(request): # TODO :: change it back
    context = RequestContext(request)
    err_code = 404
    response = render(request, 'errors/error_404.html', {'code': err_code}, context)
    response.status_code = 404
    return response
    # return render(request, 'errors/error_404.html')

# def error_500(request, exception):
def error_500(request): # TODO :: change it back
    context = RequestContext(request)
    err_code = 500
    response = render(request, 'errors/error_500.html', {'code': err_code}, context)
    response.status_code = 500
    return response
    # return render(request, 'errors/error_404.html')


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



############################################################
@login_required
def add_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)

    # if request.method == 'POST':
    request.user.books.add(book)
    return redirect('book_list')

@login_required
def delete_book(request, pk):
    book = get_object_or_404(models.Book, pk=pk)

    # if request.method == 'POST':
    request.user.books.remove(book)
    return redirect('book_list')
