from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=320)
    password = models.TextField()
    dob = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class Mail(models.Model):
    subject = models.TextField()
    content = models.TextField()
    sender = models.ForeignKey(
        User, related_name='sent_mails', on_delete=models.SET_NULL, null=True)
    receiver = models.ForeignKey(
        User, related_name='mails', on_delete=models.SET_NULL, null=True)

    sent_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'({self.sender}) - {self.subject}'
