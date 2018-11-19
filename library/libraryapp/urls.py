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
    path('', include('django.contrib.auth.urls')),
    path('signup/', views.UserCreateView.as_view(), name='signup'),
    path('signup/update/', views.UserUpdateView.as_view(), name='signup_update'),
]