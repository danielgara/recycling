from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "reset-password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/reset-password.html"
        ),
        name='password_change'
    ),
    path(
        "reset-password-done/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset-password-done.html"
        ),
        name='password_reset_done'
    ),
    path(
        "reset-password-complete/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/reset-password-finalize.html"
        ),
        name='password_reset_complete'
    ),
    path(
        'reset-password-confirm/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset-password-confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path('logout', views.custom_logout, name='accounts.logout'),
    path('login', views.custom_login, name='accounts.login'),
    path('register', views.signup, name='accounts.signup'),
    path('profile', views.profile, name='accounts.profile'),
    path('divisions', views.rankings, name='accounts.rankings'),
    path('redeem/<str:encrypted_message>', views.redemption, name='accounts.redemption'),
    path('statistics', views.stats, name='accounts.stats'),
    path('experience', views.experience_points, name='accounts.experience'),
    path('', views.index, name='accounts.index'),
    path('upload_json', views.upload_json, name='accounts.upload_json'),
    path('quiz', views.waste_quiz, name='accounts.waste_quiz'),
]
