from django.urls import path

from mailing.views import users

urlpatterns = [
    path('users', users.UsersView.as_view(), name='users'),
]