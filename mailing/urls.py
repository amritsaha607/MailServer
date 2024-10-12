from django.urls import path

from mailing.views import mails, users

urlpatterns = [
    path('users', users.UsersView.as_view(), name='users'),
    path('auth', users.AuthView.as_view(), name='auth'),
    path('mail/compose', mails.MailView.as_view(), name='compose_mail'),
]
