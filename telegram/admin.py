from django.contrib import admin
from .models import TeleGroup, UserProfile, Message

admin.site.register(TeleGroup)
admin.site.register(UserProfile)
admin.site.register(Message)
