from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin, AccessMixin
from django.contrib.auth.views import redirect_to_login
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db import transaction
from django.views.generic import (TemplateView, ListView,
                                  DetailView, CreateView,
                                  UpdateView)
from django.shortcuts import get_object_or_404, redirect, render, HttpResponseRedirect
from django.urls import reverse_lazy
# from django.contrib.auth.views import LoginView, PasswordChangeView
from django.template import RequestContext

from . import models, forms


#############################################################
# custom mixin for checking if user log out
class LogoutRequiredMixin(AccessMixin):

    def get_login_url(self):
        return reverse_lazy('user', kwargs={'pk': self.request.user.pk})

    def dispatch(self, request, *args, **kwargs):
        """
        Checks if user is not authenticated.
        """
        if request.user.is_authenticated:
            return redirect_to_login('', self.get_login_url()) # should check for alternative for '' ?
        return super(LogoutRequiredMixin, self).dispatch(request, *args, **kwargs)


#############################################################
# about this site view block
class AboutView(TemplateView):
    template_name = 'libraryapp/about.html'


#############################################################
# book block
class BookListView(ListView):
    model = models.Book
    template_name = 'libraryapp/book_list.html'

    # paginate_by = 15
    ordering = ['-release_date']

    def get_queryset(self):
        return models.Book.objects.all()


class BookDetailView(DetailView):
    model = models.Book
    template_name = 'libraryapp/book_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['comments'] = models.Comment.objects.filter(book=self.object.pk).order_by('-date')
        return context


class BookCreateView(LoginRequiredMixin, CreateView):
    model = models.Book
    form_class = forms.BookForm

    template_name = 'libraryapp/book_create.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        with transaction.atomic():
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
        with transaction.atomic():
            book = form.save() # here is some problem
            return super(BookUpdateView, self).form_valid(form)

#############################################################
# comments block
class CommentCreate(LoginRequiredMixin, CreateView):
    model = models.Comment
    form_class = forms.CommentForm

    template_name = 'libraryapp/comment_create.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})

    def form_valid(self, form):
        with transaction.atomic():
            comment = form.save()
            return super(CommentCreate, self).form_valid(form)

    # set custom data about user to the form
    def get_form(self, form_class=None):
        form_class = self.form_class
        form = super(CommentCreate, self).get_form(form_class)
        form.instance.creator = self.request.user
        form.instance.book = models.Book.objects.get(pk=self.kwargs['book_pk'])
        return form


class ReplyCreate(LoginRequiredMixin, CreateView):
    model = models.Comment
    form_class = forms.CommentForm

    template_name = 'libraryapp/comment_create.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})

    def form_valid(self, form):
        with transaction.atomic():
            comment = form.save()
            return super(ReplyCreate, self).form_valid(form)

    # set custom data about user to the form
    def get_form(self, form_class=None):
        form_class = self.form_class
        form = super(ReplyCreate, self).get_form(form_class)
        form.instance.creator = self.request.user
        form.instance.book = models.Book.objects.get(pk=self.kwargs['book_pk'])
        form.instance.parent_comment = models.Comment.objects.get(pk=self.kwargs['reply_pk'])
        return form


class CommentUpdate(UserPassesTestMixin, LoginRequiredMixin, UpdateView):
    model = models.Comment
    form_class = forms.CommentForm

    template_name = 'libraryapp/comment_update.html'

    login_url = '/login/'

    def get_success_url(self):
        return reverse_lazy('book_detail', kwargs={'pk': self.object.book.pk})

    def form_valid(self, form):
        with transaction.atomic():
            comment = form.save()
            return super(CommentUpdate, self).form_valid(form)

    def get_object(self, queryset=None):
        return models.Comment.objects.get(pk=self.kwargs['pk'])
        # return models.CustomUser.objects.get(pk=self.request.user.pk)

    # only owner of a post can delete it
    def test_func(self):
        comment = models.Comment.objects.get(pk=self.kwargs['pk'])
        return comment.creator == self.request.user

@login_required
def comment_delete(request, pk):
    with transaction.atomic():
        comment = models.Comment.objects.get(pk=pk)
        if comment.creator == request.user:
            comment.delete()
            messages.success(request, 'Comment was deleted.')
        else:
            messages.error(request, 'You don\'t have right to edit this comment')
    next_url = request.GET.get('next', '/')
    return HttpResponseRedirect(next_url)


#############################################################
# author block
class AuthorListView(ListView):
    model = models.Author
    template_name = 'libraryapp/author_list.html'

    # paginate_by = 15
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
        with transaction.atomic():
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
        with transaction.atomic():
            author = form.save() # here is some problem
            return super(AuthorUpdateView, self).form_valid(form)


#############################################################
# user authentication block

class UserCreateView(LogoutRequiredMixin, CreateView):
    model = models.CustomUser
    form_class = forms.CustomUserCreationForm
    template_name = 'registration/signup.html'


    def get_success_url(self):
        return reverse_lazy('user', kwargs={'pk': self.object.pk})

    def form_valid(self, form):
        with transaction.atomic():
            user = form.save()
            return super(UserCreateView, self).form_valid(form)


class UserUpdateView(LoginRequiredMixin, UpdateView):
    model = models.CustomUser
    form_class = forms.CustomUserUpdateForm
    template_name = 'registration/user_update.html'

    login_url = '/login/'


    # get the account of this user
    def get_object(self, queryset=None):
        return models.CustomUser.objects.get(pk=self.request.user.pk)

    def get_success_url(self):
        return reverse_lazy('user', kwargs={'pk': self.request.user.pk})

    # send the data to the db via post
    def form_valid(self, form):
        with transaction.atomic():
            user = form.save() # here is some problem
            return super(UserUpdateView, self).form_valid(form)


class UserDetailView(LoginRequiredMixin, DetailView):
    model = models.CustomUser
    template_name = 'registration/user_detail.html'
    login_url = '/login/'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = self.object.books.all
        return context



# class UserLoginView(LogoutRequiredMixin, LoginView):
#     form_class = forms.CustomUserLoginForm
#     template_name = 'registration/login.html'
#
#     # login_url = 'books'
#
#     # def get_login_url(self):
#     #     return reverse_lazy('user', kwargs={'pk': self.request.user.pk })



# class UserChangePasswordView(LoginRequiredMixin, PasswordChangeView):
#     form_class = forms.CustomUserChangePassword
#     template_name = 'registration/change_password.html'
#
#     login_url = '/login/'
#
#
#     def get_success_url(self):
#         return reverse_lazy('about')
#
#     def form_valid(self, form):
#         with transaction.atomic():
#             user = form.save()
#             return super(UserChangePasswordView, self).form_valid(form)
#
#     # # check if this user is owner of the form they want to access
#     # def test_func(self):
#     #     return self.kwargs['pk'] == self.request.user.pk

@login_required
def user_delete(request):
    with transaction.atomic():
        u = models.CustomUser.objects.get(pk=request.user.pk)
        u.delete()
    messages.success(request, 'User was deleted.')
    return redirect('about')


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
#
# @login_required
# def add_comment_to_book(request, pk):
#     book = get_object_or_404(models.Book, pk=pk)
#
#     if request.method == 'POST':
#         form = forms.CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.book = book
#             comment.save()
#             return redirect('post_detail', pk=book.pk)
#     else:
#         form = forms.CommentForm()
#     return render(request, 'libraryapp/comment_form.html', {'form': form})
#
# @login_required
# def remove_comment(request, pk):
#     comment = get_object_or_404(models.Comment, pk=pk)
#     book_pk = comment.book.pk
#     comment.delete()
#     return redirect('book_detail', pk=book_pk)



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
