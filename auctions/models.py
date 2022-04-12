from email.mime import image
from email.policy import default
from tkinter import CASCADE
from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=128)
    description = models.CharField(max_length=1000)
    category =models.ForeignKey('Category', on_delete=models.PROTECT)
    status = models.BooleanField(default=True, blank=True)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
    picture = models.ImageField(upload_to='',blank=True, null = True)
    price = models.FloatField(blank=False, default=0, null=True)
    winner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    
    def __str__(self):
        return self.title

class Bid(models.Model):
    bids = models.FloatField(blank=False, default=0)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    
class Comment(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE)
    comment = models.CharField(max_length=128, blank=True)
class Watchlist(models.Model):
    user_id = models.ForeignKey(User, on_delete=models.CASCADE, related_name="watchlist")
    listing_id = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="listings")
    def __str__(self):
        return self.listing_id.title
    
class Category(models.Model):
    cat = models.CharField(max_length=128,default='SOME STRING')
    def __str__(self):
        return self.cat
    