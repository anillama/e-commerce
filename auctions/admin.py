from django.contrib import admin

# Register your models here.

from .models import Categories, Auction, Bid, User, Comments, WatchList, Closed_case

class CommetData(admin.ModelAdmin):
	list_display = ("userName", "comments", "timeDate", "prodId")

class CategoriesData(admin.ModelAdmin):
	list_display = ("nameCata", )

class UserData(admin.ModelAdmin):
	list_display = ("id", "username", "date_joined")

class AuctionData(admin.ModelAdmin):
	list_display = ("id", "title", "discription", "price", "category", "image", "userName")

class BidData(admin.ModelAdmin):
	list_display = ("userName", "bidPrice", "productId")

class WatchId(admin.ModelAdmin):
	list_display = ("user", "id")

class Closed(admin.ModelAdmin):
	list_display = ("userName", "itemNumb", "itemStat")

admin.site.register(Categories, CategoriesData)
admin.site.register(Auction, AuctionData)
admin.site.register(Bid, BidData)
admin.site.register(User, UserData)
admin.site.register(Comments, CommetData)
admin.site.register(WatchList, WatchId)
admin.site.register(Closed_case, Closed)
