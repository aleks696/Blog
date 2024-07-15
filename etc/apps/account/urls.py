from django.urls import path, include
from .views import (authView, login_view, logout_view, send_friend_request, delete_account)
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('login/', login_view, name='login'),
    path('registration/', authView, name='authView'),
    path('logout/', logout_view, name='logout'),
    path('profile/', views.profile_view, name='profile'),
    path('profile/<str:username>/', views.author_profile_view, name='author_profile'),
    path('profile/<str:username>/add_friend/', views.send_friend_request, name='send_friend_request'),
    path('profile/<str:username>/remove_friend/', views.remove_friend, name='remove_friend'),
    path('friend_request/<int:request_id>/accept/', views.accept_friend_request, name='accept_friend_request'),
    path('friend_request/<int:request_id>/decline/', views.decline_friend_request, name='decline_friend_request'),
    path('friend_request/<int:request_id>/cancel/', views.cancel_friend_request, name='cancel_friend_request'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uid64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
    path('send_friend_request/<username>/', send_friend_request, name='send_friend_request'),
    path('delete_account/', delete_account, name='delete_account'),
]
