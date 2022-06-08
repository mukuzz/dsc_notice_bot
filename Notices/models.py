from django.db import models
from django.utils import timezone

# Create your models here.

class Notice(models.Model):
	date = models.DateTimeField(default=timezone.now)
	title = models.CharField(max_length=1024)
	key = models.CharField(primary_key=True, unique=True, max_length=32)
	content = models.TextField()
	url = models.CharField(max_length=1024) # Source Address

	def __str__(self):
		return self.title
