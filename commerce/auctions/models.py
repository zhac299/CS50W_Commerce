from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass
    def __str__(self):
        return f"{self.username}, {self.password}, {self.email}"

class auction_listing(models.Model):
    name = models.CharField(max_length=512)
    poster = models.ForeignKey(User, on_delete=models.CASCADE)
    desc = models.TextField(blank=True)
    price = models.DecimalField(max_digits=13, decimal_places=2)
    image_url = models.TextField(blank=True)
    category = models.CharField(max_length=64)
    closed = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name}, {self.poster}, {self.desc}, {self.price}, {self.image_url}"

class watchlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=512)
    item_id = models.IntegerField()

    def __str__(self):
        return f"{self.item_name}"

class wonitems(models.Model):
    won_username = models.ForeignKey(User, on_delete=models.CASCADE)
    item_name = models.CharField(max_length=512)
    won_items_price = models.DecimalField(max_digits=13, decimal_places=2)

class bids(models.Model):
    username = models.ForeignKey(User, on_delete=models.CASCADE)
    starting = models.DecimalField(max_digits=13, decimal_places=2, default=None)
    price = models.DecimalField(max_digits=13, decimal_places=2)

    def __str__(self):
        return f"{self.username}, {self.starting}, {self.price}"

class comments(models.Model):
    username = models.CharField(max_length=512)
    listing_item = models.ForeignKey(auction_listing, on_delete=models.CASCADE, blank=True)
    user_comment = models.TextField()

    def __str__(self):
        return f"{self.username}, {self.user_comment}"