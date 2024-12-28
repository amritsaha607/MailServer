from django.urls import path

from mailing.consumers import mails

urlpatterns = [
    path('ws/mail/<str:user>', mails.MailConsumer.as_asgi()),
]
