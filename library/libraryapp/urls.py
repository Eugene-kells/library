from django.urls import path, include

from . import views

urlpatterns = [
    path('', views.AboutView.as_view(), name='about'),
    # book block
    path('books/', views.BookListView.as_view(), name='book_list'),
    path('book/<int:pk>/', views.BookDetailView.as_view(), name='book_detail'),
    path('book/new/', views.BookCreateView.as_view(), name='book_new'),
    path('book/<int:pk>/update/', views.BookUpdateView.as_view(), name='book_update'),
    # book-comment block
    path('book/<int:pk>/comment/', views.add_comment_to_book, name='add_comment_to_book'),
    # comment block
    path('comment/<int:pk>/remove/', views.remove_comment, name='remove_comment'),
    # author block
    path('authors/', views.AuthorListView.as_view(), name='author_list'),
    path('author/<int:pk>/', views.AuthorDetailView.as_view(), name='author_detail'),
    path('author/new/', views.AuthorCreateView.as_view(), name='author_new'),
    path('author/<int:pk>/update/', views.AuthorUpdateView.as_view(), name='author_update'),
    # authentication block TODO :: make a different app for that
    path('login/', views.UserLoginView.as_view(), name='login'), # here I redefine one instance of next line (included)
    # need to consider another variant later
    path('', include('django.contrib.auth.urls')), # login, logout and reset password
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('user/<int:pk>/', views.UserDetailView.as_view(), name='user'),
    path('user/chngpswd/<int:pk>/', views.UserChangePasswordView.as_view(), name='change_password'),
    path('user/update/<int:pk>/', views.UserUpdateView.as_view(), name='user_update'),
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



