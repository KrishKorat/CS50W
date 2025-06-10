from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from .models import Listing, Bid, Comment
from .forms import ListingForm

from .models import User
from django.contrib.auth.decorators import login_required



def index(request):
    active_listing = Listing.objects.filter(is_active=True)
    return render(request, "auctions/index.html", {
        "listings": active_listing
    })



def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")



def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))



def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")



@login_required
def create_listing(request):

    if request.method == "POST":
        form = ListingForm(request.POST)

        if form.is_valid():
            listing = form.save(commit=False)
            listing.creator = request.user
            listing.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = ListingForm()
    
    return render(request, "auctions/create_listing.html", {
        "form": form
    })




def listing(request, listing_id):
    listing = Listing.objects.get(pk=listing_id)
    comments = listing.comments.all()
    # user_is_watching = request.user in listing.watchlist.all()
    highest_bid = listing.bids.order_by('-amount').first()
    highest_bidder = highest_bid.bidder if highest_bid else None


    if request.method == "POST":

        if "place_bid" in request.POST:
            amount = float(request.POST["bid_amount"])
            min_bid = listing.starting_bid
            if highest_bid:
                min_bid = max(listing.starting_bid, highest_bid.amount + 0.01)
            
            if amount >= min_bid:
                Bid.objects.create(
                    listing = listing,
                    bidder = request.user,
                    amount = amount
                )
            else:
                return render(request, 'auctions/listing.html', {
                    "listing": listing,
                    "comment": comments,
                    "highest_bidder": highest_bidder,
                    "error": f"Your bid must be at least {min_bid}"
                })
        
        elif "add_watchlist" in request.POST:
            listing.watchlist.add(request.user)
        
        elif "remove_watchlist" in request.POST:
            listing.watchlist.remove(request.user)

        
        elif "close_auction" in request.POST and request.user == listing.creator:
            listing.is_active = False
            if highest_bid:
                listing.winner = highest_bid.bidder
            listing.save()
        

        elif "add_comment" in request.POST:
            content = request.POST["comment"]
            Comment.objects.create(
                listing = listing,
                author = request.user,
                content = content
            )
        

        return redirect('listing', listing_id=listing.id)




    return render(request, 'auctions/listing.html', {
        "listing": listing,
        "comments": comments,
        "highest_bidder": highest_bidder
    })