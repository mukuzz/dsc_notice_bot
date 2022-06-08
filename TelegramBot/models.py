from django.db import models
from Notices.models import Notice

# Create your models here.

class SentNotice(models.Model):
	key = models.CharField(primary_key=True, unique=True, max_length=32)
	notice = models.ForeignKey(Notice, on_delete=models.CASCADE)


class BotUser(models.Model):
	user_id = models.IntegerField(primary_key=True)
	first_name = models.CharField(max_length=200)
	last_name = models.CharField(max_length=200, blank=True)
	is_bot = models.BooleanField()
	join_date_time = models.DateTimeField()

	def __str__(self):
		return self.first_name
