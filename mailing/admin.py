from django.contrib import admin

from .models import MailEvent, MailItem, RawEvent, User

admin.site.register(User)
admin.site.register(MailEvent)
admin.site.register(MailItem)
admin.site.register(RawEvent)
