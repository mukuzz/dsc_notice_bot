from django.db import models

# Create your models here.

class Notice(models.Model):
	title = models.CharField(max_length=200)
	key = models.IntegerField(default=0)
	content = models.CharField(max_length=200) # Website Address

	def __str__(self):
		return self.title

	def getKey(self):
		return self.key