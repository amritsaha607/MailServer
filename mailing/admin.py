from django.contrib import admin

from .models import MailEvent, MailItem, User

admin.site.register(User)
admin.site.register(MailEvent)
admin.site.register(MailItem)
