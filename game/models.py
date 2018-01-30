from __future__ import unicode_literals

from django.db import models

# Create your models here.

class details(models.Model):
	name = models.CharField(max_length = 250)
	email = models.CharField(max_length = 100)
	phone = models.CharField(max_length= 20)

	def __str__(self):
		return self.name

class scores(models.Model):
	user = models.ForeignKey('details')
	score = models.IntegerField()
	win = models.BooleanField()
	date = models.DateTimeField(auto_now_add= True)

	def __str__(self):
		return str(self.score)