from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    # book block
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book_new'),
    path('book/update/<int:pk>/', views.BookUpdateView.as_view(), name='book_update'),
    # book-user block  | shouldn't do this as POST?
    path('book/add/<int:pk>/', views.add_book, name='add_user_book'),
    path('book/delete/<int:pk>/', views.delete_book, name='delete_user_book'),
    # comment block
    path('comment/create/<int:book_pk>/', views.CommentCreate.as_view(), name='create_comment'),
    path('comment/create/<int:book_pk>/<int:reply_pk>/', views.ReplyCreate.as_view(), name='create_reply'),
    path('comment/update/<int:pk>/', views.CommentUpdate.as_view(), name='update_comment'),
    path('comment/remove/<int:pk>/', views.comment_delete, name='delete_comment'),
    # author block
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/new/', views.AuthorCreateView.as_view(), name='author_new'),
    path('author/update/<int:pk>/', views.AuthorUpdateView.as_view(), name='author_update'),
    # authentication block TODO :: make a different app for that
    # path('login/', views.UserLoginView.as_view(), name='login'), # here I redefine one instance of url (in auth.urls)
    # path('user/chngpswd/', views.UserChangePasswordView.as_view(), name='change_password'),
    # need to consider another variant later
    # this urls includes login, logout, change password and reset password staff
    path('', include('django.contrib.auth.urls')), # login, logout and reset password (default by Django)
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('user/update/', views.UserUpdateView.as_view(), name='user_update'),
    path('user/delete/', views.user_delete, name='user_delete'),
    # error block (it shouldnt be here)
    # path('400/', views.error_400, name='error400'),
    # path('403/', views.error_403, name='error403'),
    # path('404/', views.error_404, name='error404'),
    # path('500/', views.error_500, name='error500'),
]

# handlers for different errors
handler400 = 'libraryapp.views.error_400'
handler403 = 'libraryapp.views.error_403'
handler404 = 'libraryapp.views.error_404'
handler500 = 'libraryapp.views.error_500'



