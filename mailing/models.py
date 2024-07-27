from django.db import models
from django.utils import timezone


class User(models.Model):
    name = models.CharField(max_length=30)
    email = models.EmailField(max_length=320, unique=True)
    password = models.CharField(max_length=512)
    dob = models.DateTimeField(default=timezone.now)

    created_at = models.DateTimeField(default=timezone.now)
    updated_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.email


class MailEvent(models.Model):
    chain_id = models.CharField(max_length=36, db_index=True)
    subject = models.TextField()
    content = models.TextField()
    sender = models.ForeignKey(User,
                               related_name="sent_mail_events",
                               on_delete=models.SET_NULL,
                               null=True)
    receivers = models.ManyToManyField(User,
                                       related_name="received_mail_events",
                                       on_delete=models.SET_NULL,
                                       null=True)
    sent_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.sender}) - {self.subject}"


class MailItem(models.Model):
    chain_id = models.CharField(max_length=36, db_index=True)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name="mails")
    event = models.ForeignKey(MailEvent,
                              on_delete=models.CASCADE,
                              related_name="mail_items")
    is_sent = models.BooleanField()
    timestamp = models.DateTimeField()
    content = models.TextField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user} - {self.event.subject}"
