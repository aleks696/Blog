from django.urls import path
from . import views

urlpatterns = [
    path('', views.post_view, name='posts'),
    path('<int:pk>/', views.post_detail, name="post_detail"),
    path('post/create/', views.create_post_view, name='create_post'),
    path('post/<int:pk>/delete/', views.delete_post, name='delete_post'),
    path('post/<int:pk>/edit/', views.edit_post_view, name='edit_post'),
    path('search/', views.search_posts, name='search_posts'),
    path('review/<int:pk>/', views.add_comments, name='add_comments'),
    path('<int:pk>/add_likes/', views.add_like, name='add_likes'),
    path('<int:pk>/dislikes/', views.dislike, name='dislikes'),
]
