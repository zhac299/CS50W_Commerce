from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

import decimal
from decimal import Decimal

from .models import User, auction_listing, bids, comments, watchlist, wonitems


def index(request):
    auction_lists = auction_listing.objects.filter(closed=False)    
    return render(request, "auctions/index.html", {
        "auction_list": auction_lists
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

def create(request, user):
    if request.method == "POST":
        item_name = request.POST["item_name"]
        item_desc = request.POST["item_desc"]
        item_price = request.POST["item_price"]
        item_url = request.POST["item_pic"]
        item_cat = request.POST["categories"]

        if item_name == "" or item_name is None:
            return render(request, "auctions/create.html", {
                "msgErr1": "Please enter a title"
            })
        elif item_price is None or item_price == "":
            return render(request, "auctions/create.html", {
                "msgErr2": "Please enter a price"
            })

        # create new entry in auction_listing
        item = auction_listing()
        item.name = item_name
        item.price = item_price
        item.image_url = item_url
        item.desc = item_desc
        item.poster = request.user
        item.closed = False
        item.category = item_cat
        item.save()

        # create new entry in bid
        bid = bids()
        bid.username = request.user
        bid.starting = item_price
        bid.price = item_price
        bid.save()

    return render(request, "auctions/create.html", {
        "msg": "Listing Posted"    
    })

def listing(request, id):
    item = auction_listing.objects.get(id=id)
    bid = bids.objects.get(id=id)
    commentsdb = comments.objects.filter(listing_item=item)
    itemPosterUsername = User.objects.get(id=item.poster_id)
    if request.method == "POST":
        if "deleteListing" in request.POST:
            if bid.username == item.poster:
                item.closed = True
                newWin = wonitems(won_username=request.user, item_name=item.name, won_items_price=0)
                item.save()
                newWin.save()
                return render(request, "auctions/listing.html", {
                    "msgDel": "Listing Removed " + item.poster + " Removed Listing",
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username #()
                })
            else:
                bidWinner = bid.username_id
                item.closed = True
                winningUser = User.objects.get(id=bidWinner) #()
                newWin = wonitems(won_username=winningUser, item_name=item.name, won_items_price=bid.price)
                item.save()
                newWin.save()
                winningUsername = winningUser.username
                return render(request, "auctions/listing.html", {
                    "msgDel": "Listing Removed " + winningUsername + " Won Item", #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username #()
                })    
        elif "watchlistBut" in request.POST:
            if watchlist.objects.filter(user=request.user, item_name=item.name).exists():
                return render(request, "auctions/listing.html", {
                    "listing_id": item.id,
                    "listing_name": item.name,
                    "listing_desc": item.desc,
                    "listing_price": item.price,
                    "listing_url": item.image_url,
                    "bid_price_min": item.price,
                    "og_poster": itemPosterUsername.username, #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username, #()
                    "msg": "Item already in Watchlist",
                    "comments": commentsdb,
                    "category": item.category
                })
            else:
                watchlistV = watchlist(user=request.user, item_name=item.name, item_id=item.id)
                watchlistV.save()
                return HttpResponseRedirect(reverse("watchlistView"))
        elif "submitBid" in request.POST:                
            if item.price < Decimal(request.POST["bid"]):           
                bid.price = str(request.POST["bid"])
                bid.username = request.user #()
                item.price = request.POST["bid"]
                item.save()
                bid.save()
                return render(request, "auctions/listing.html", {
                    "listing_id": item.id,
                    "listing_name": item.name,
                    "listing_desc": item.desc,
                    "listing_price": item.price,
                    "listing_url": item.image_url,
                    "bid_price_min": item.price,
                    "og_poster": itemPosterUsername.username, #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username, #()
                    "comments": commentsdb,
                    "category": item.category
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing_id": item.id,
                    "listing_name": item.name,
                    "listing_desc": item.desc,
                    "listing_price": item.price,
                    "listing_url": item.image_url,
                    "bid_price_min": item.price,
                    "msg": "Enter a bid greater than the current bid",
                    "og_poster": itemPosterUsername.username, #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username, #()
                    "comments": commentsdb,
                    "category": item.category
                })
        elif "commentSubmit" in request.POST:
            thecomment = request.POST["commentArea"]
            if thecomment != "" or thecomment != " " or thecomment != None:
                commentstorage = comments()
                commentstorage.username = request.user.username #()
                commentstorage.listing_item = item
                commentstorage.user_comment = thecomment
                commentstorage.save()
                commentsdb = comments.objects.filter(listing_item=item)
                return render(request, "auctions/listing.html", {
                    "listing_id": item.id,
                    "listing_name": item.name,
                    "listing_desc": item.desc,
                    "listing_price": item.price,
                    "listing_url": item.image_url,
                    "bid_price_min": item.price,
                    "msg": "Comment Submitted",
                    "og_poster": itemPosterUsername.username, #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username, #()
                    "comments": commentsdb,
                    "category": item.category
                })
            else:
                return render(request, "auctions/listing.html", {
                    "listing_id": item.id,
                    "listing_name": item.name,
                    "listing_desc": item.desc,
                    "listing_price": item.price,
                    "listing_url": item.image_url,
                    "bid_price_min": item.price,
                    "msg": "Invalid Comment",
                    "og_poster": itemPosterUsername.username, #()
                    "checkClosed": item.closed,
                    "currentUser": request.user.username,
                    "owner": itemPosterUsername.username, #()
                    "comments": commentsdb,
                    "category": item.category
                })
    else:
        return render(request, "auctions/listing.html", {
            "listing_id": item.id,
            "listing_name": item.name,
            "listing_desc": item.desc,
            "listing_price": item.price,
            "listing_url": item.image_url,
            "bid_price_min": item.price,
            "og_poster": itemPosterUsername.username, #()
            "checkClosed": item.closed,
            "currentUser": request.user.username,
            "owner": itemPosterUsername.username, #()
            "comments": commentsdb,
            "category": item.category
        })

def watchlistView(request):
    newWatchlist = watchlist.objects.filter(user=request.user)

    for item in newWatchlist:
        itemname = str(item.item_name)
        
        if request.method == "POST" and "delete-"+itemname:
            watchlist.objects.filter(item_name=item.item_name).delete()
            newWatchlist = watchlist.objects.filter(user=request.user)
            return render(request, "auctions/watchlist.html", {
                "watchlistV": newWatchlist
            })
        else:
            return render(request, "auctions/watchlist.html", {
                "watchlistV": newWatchlist,
            })

    return render(request, "auctions/watchlist.html", {
        "msg": "Your Watchlist is Empty",
   })


def profile(request):
    user_wonitems = wonitems.objects.filter(won_username_id=request.user.id)
    total_cost = 0

    for item in user_wonitems:
        total_cost += item.won_items_price

    return render(request, "auctions/profile.html", {
        "user_items": user_wonitems,
        "total": total_cost
    })

def categoriesDisplay(request):
    items = auction_listing.objects.filter(closed=False)
    catList = []
    for item in items:
        if item.category not in catList:
            catList.append(item.category)
    return render(request, "auctions/categories.html", {
        "catList": catList
    })

def specificcat(request, cat):
    catItem = auction_listing.objects.filter(category=cat)
    return render(request, "auctions/specificcat.html", {
        "catItem": catItem,
        "catName": cat
    })