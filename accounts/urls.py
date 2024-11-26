from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    path(
        "resetear-password/",
        auth_views.PasswordResetView.as_view(
            template_name="accounts/reset-password.html"
        ),
        name='password_change'
    ),
    path(
        "resetear-password-completado/",
        auth_views.PasswordResetDoneView.as_view(
            template_name="accounts/reset-password-done.html"
        ),
        name='password_reset_done'
    ),
    path(
        "resetear-password-finalizado/",
        auth_views.PasswordResetCompleteView.as_view(
            template_name="accounts/reset-password-finalize.html"
        ),
        name='password_reset_complete'
    ),
    path(
        'resetear-password-confirmacion/<uidb64>/<token>/',
        auth_views.PasswordResetConfirmView.as_view(
            template_name='accounts/reset-password-confirm.html'
        ),
        name='password_reset_confirm'
    ),
    path('cerrar-sesion', views.custom_logout, name='accounts.logout'),
    path('iniciar-sesion', views.custom_login, name='accounts.login'),
    path('registro', views.signup, name='accounts.signup'),
    path('perfil', views.profile, name='accounts.profile'),
    path('divisiones', views.rankings, name='accounts.rankings'),
    path('redimir/<str:encrypted_message>', views.redemption, name='accounts.redemption'),
    path('estadisticas', views.stats, name='accounts.stats'),
    path('experiencia', views.experience_points, name='accounts.experience'),
    path('', views.index, name='accounts.index'),
    path('cargar_json', views.upload_json, name='accounts.upload_json'),
    path('quiz', views.waste_quiz, name='accounts.waste_quiz'),
]
