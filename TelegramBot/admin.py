from django.contrib import admin

# Register your models here.
from .models import BotUser

class BotUserAdmin(admin.ModelAdmin):
	list_display = ('user_id', 'first_name', 'last_name', 'join_date_time', 'is_bot')
	ordering = ('-join_date_time',)

admin.site.register(BotUser, BotUserAdmin)