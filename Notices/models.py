from django.db import models

# Create your models here.

class Notice(models.Model):
	title = models.CharField(max_length=200)
	key = models.CharField(unique=True, max_length=32)
	content = models.TextField()
	url = models.CharField(max_length=200) # Source Address

	def __str__(self):
		return self.title
