from django.db import models
from django.conf import settings
from django.utils import timezone
from django.contrib.auth.models import User
from django.urls import reverse

class Post(models.Model):
	#author=models.CharField(max_length=16, null=False)
	author=models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	title=models.CharField(max_length=200)
	text=models.TextField();
	created_date=models.DateTimeField(default=timezone.now)
	published_date=models.DateTimeField(blank=True, null=True)
	favorite=models.ManyToManyField(User, related_name='like_post',blank=True)

	def publish(self):
		self.published_date=timezone.now()
		self.save()
	def __str__(self):
		return self.title

class Bookmark(models.Model):
	name=models.CharField(max_length=100)
	url=models.URLField('Site URL')

	def __str__(self):
		return "name: "+self.name+", 주소: "+self.url