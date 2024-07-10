from django.urls import path, include
from .views import authView, login_view, logout_view, profile_view
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include("django.contrib.auth.urls")),
    path('login/', login_view, name='login'),
    path('registration/', authView, name='authView'),
    path('logout/', logout_view, name='logout'),
    path('profile/', profile_view, name='profile'),
    path('password_reset/', auth_views.PasswordResetView.as_view(template_name='accounts/password_reset_form.html'), name="password_reset"),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name="password_reset_done"),
    path('reset/<uid64>/<token>', auth_views.PasswordResetConfirmView.as_view(), name="password_reset_confirm"),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name="password_reset_complete"),
]
