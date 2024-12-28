from django.urls import path

from mailing.consumers import mail

urlpatterns = [
    path('ws/mail/<str:user>', mail.MailConsumer.as_asgi()),
]
