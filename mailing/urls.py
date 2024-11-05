from django.urls import path

from mailing.views import mails, users

urlpatterns = [
    path('users', users.UsersView.as_view(), name='users'),
    path('auth', users.AuthView.as_view(), name='auth'),
    path('mails', mails.FetchMailView.as_view(), name='mails'),
    path('mail/compose', mails.ComposeMailView.as_view(), name='compose_mail'),
]
