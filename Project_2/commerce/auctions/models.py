from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass


class Listing(models.Model):

    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.DecimalField(max_digits=10, decimal_places=2)
    image_url = models.URLField(blank=True, null=True)
    category = models.CharField(max_length=64, blank=True, null=True)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, related_name="listing")
    is_active = models.BooleanField(default=True)
    winner = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL, related_name="won_listing")
    watchlist = models.ManyToManyField(User, blank=True, related_name="watchlist")

    def __str__(self):
        return f"{self.title} - Active: {self.is_active}"
    


class Bid(models.Model):

    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="bids")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bid_user")
    amount = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.amount} by {self.bidder} on {self.listing.title}"
    



class Comment(models.Model):
    
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="comment")
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name="comment")
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.author} on {self.listing.title}"