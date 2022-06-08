from django.contrib import admin

# Register your models here.
from .models import Notice

class NoticeAdmin(admin.ModelAdmin):
	list_display = ('date','title','url')
	ordering = ('-date',)
	#list_filter = ['pub_date']

admin.site.register(Notice, NoticeAdmin)