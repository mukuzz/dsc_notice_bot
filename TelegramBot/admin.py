from django.contrib import admin

# Register your models here.
from .models import BotUser, SentNotice

class BotUserAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'first_name', 'last_name', 'join_date_time', 'is_bot')
	ordering = ('-join_date_time',)

class SentNoticeAdmin(admin.ModelAdmin):
	list_display = ('key', 'notice')

admin.site.register(BotUser, BotUserAdmin)
admin.site.register(SentNotice, SentNoticeAdmin)