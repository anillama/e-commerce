from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import datetime, date
from django.conf import settings

class User(AbstractUser):
    pass

class Categories(models.Model):
	nameCata = models.CharField(max_length=65)
	def __str__(self):
		return f'{self.nameCata}'

class Auction(models.Model):
	title = models.CharField(max_length=65)
	discription = models.TextField(null=True)
	price = models.DecimalField(null=False, max_digits=8, decimal_places=2)
	category = models.ForeignKey(Categories, on_delete=models.CASCADE, null=False)
	image = models.ImageField(upload_to='collectionMedia/', null=True, blank=True)
	userName = models.CharField(max_length=65, null=False)
	
	def __str__(self):
		return f'{self.title}, {self.discription}, {self.price}, {self.category}, {self.image}'

class Bid(models.Model):
	userName = models.CharField(max_length=65)
	bidPrice = models.DecimalField(null=False, max_digits=8, decimal_places=2)
	productId = models.IntegerField()

	def __str__(self):
		return f'{self.userName}, {self.bidPrice}'


class Comments(models.Model):
	userName = models.CharField(max_length=65)
	comments = models.CharField(max_length=200)
	timeDate = models.DateTimeField(auto_now_add=True, auto_now=False, blank=True)
	prodId   = models.CharField(max_length=5, default=None)

	def __str__(self):
		return f'{self.userName}, {self.comments}, {self.timeDate}'

class WatchList(models.Model):
	user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	listItem = models.ManyToManyField(Auction)

	def __str__(self):
		return f'{self.user}'

class Closed_case(models.Model):
	userName = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
	itemNumb = models.IntegerField()
	itemStat = models.CharField(max_length=20)

	def __str__(self):
		return f'{self.userName}, {self.itemNumb}, {self.itemStat}'