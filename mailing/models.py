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

    def get_json_data(self):
        return {
            'name': self.name,
            'email': self.email,
            'dob': self.dob,
        }


class RawEvent(models.Model):
    chain_id = models.CharField(max_length=36, db_index=True)
    payload = models.TextField()
    received_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f'{self.chain_id} - {self.received_at}'


class MailEvent(models.Model):
    chain_id = models.CharField(max_length=36, db_index=True)
    subject = models.TextField()
    content = models.TextField()
    sender = models.ForeignKey(User,
                               related_name="sent_mail_events",
                               on_delete=models.SET_NULL,
                               null=True)
    receivers = models.ManyToManyField(User,
                                       related_name="received_mail_events")
    sent_at = models.DateTimeField()

    created_at = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"({self.sender}) - {self.subject}"

    def get_json_data(self):
        return {
            'chain_id': self.chain_id,
            'subject': self.subject,
            'sender': self.sender.email,
            'receivers': [receiver.email for receiver in self.receivers.all()],
            'sent_at': self.sent_at,
        }


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
