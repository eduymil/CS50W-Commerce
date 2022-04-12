from operator import truediv
from telnetlib import STATUS
from unicodedata import category
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.db.models import Max
from django import forms
from django.core.files.uploadedfile import SimpleUploadedFile

from .models import Bid, Category, User, Listing, Bid, Comment, Watchlist
from django import forms
from PIL import Image
from django.contrib.auth.decorators import login_required

class listform(forms.Form):
    title = forms.CharField(label='Title', max_length=128)
    description =forms.CharField(label='Description', max_length=1000)
    start_bid = forms.FloatField(label='Starting Bid')
    picture = forms.ImageField()
class Bidform(forms.Form):
    bid = forms.FloatField(label='Bid')


def index(request):
    all = Listing.objects.filter(status = True)
    user = User.objects.all()
    cat = Category.objects.all()
    return render(request, "auctions/index.html",{
        "listing":all,
        "cat":cat
    })

def inactive(request):
    all = Listing.objects.filter(status = False)
    user = User.objects.all()
    return render(request, "auctions/inactive.html",{
        "listing":all
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

def create(request):
    if request.method == "POST":
        form = listform(request.POST or None, request.FILES or None)
        # image = request.POST.get('picture')
        cat = Category.objects.get(pk=request.POST.get('category'))
        user = request.user
        if form.is_valid():
            new = Listing.objects.create(
                # picture = image,
                picture = form.cleaned_data['picture'],
                user_id = user,
                title =form.cleaned_data['title'],
                description =form.cleaned_data['description'],
                price =form.cleaned_data['start_bid'],    
                category=cat            
            )
            new.save()
            return HttpResponseRedirect(reverse("index"))
    else:     
        form = listform()
        cat = Category.objects.all()
        return render(request, "auctions/create.html",{
            'form':form,
            'category':cat
        })
def indi(request, user, title):
    list = Listing.objects.get(pk=title)
    user = list.user_id
    comments = Comment.objects.filter(listing_id = title)
    if request.user.is_authenticated:
        test = Watchlist.objects.filter(
                user_id = request.user,
                listing_id = Listing.objects.get(pk = title)
            )
        if test:
            wl = True
        else:
            wl = False
    else:
        wl = False
    form = Bidform()
    ls = Bid.objects.filter(listing_id=title)
    start = Listing.objects.get(pk=title)
    start = start.price
    ls = ls.aggregate(Max('bids'))
    if ls['bids__max'] is None:
        #min value = starting bid
        highest = start
        check = start
        got_bid = False
    else:
        highest=ls['bids__max']
        check= highest+ 0.01
        got_bid = True
    return render(request,"auctions/post.html",{
        'listings':list,
        'comments':comments,
        'wl':wl,
        'form':form,
        'highest':highest,
        'check':check,
        'got_bid':got_bid
    })
@login_required
def comment(request):
    if request.method == "POST":    
        listing = Listing.objects.get(pk = (request.POST.get('id')))
        new = Comment.objects.create(
            user_id = request.user,
            listing_id = listing,
            comment = request.POST.get('comment')
        )
        new.save()
        return HttpResponseRedirect(reverse("indi", kwargs={'user':listing.user_id,'title':listing.id}))
@login_required
def watchlist(request,user):
    if request.method =="POST":
        test = Watchlist.objects.filter(
            user_id = request.user,
            listing_id = Listing.objects.get(pk = int(request.POST.get('id')))
        )
        #if not in watchlist create
        if not test:
            new = Watchlist.objects.create(
                user_id = request.user,
                listing_id = Listing.objects.get(pk = int(request.POST.get('id')))
            )
            new.save()
            return HttpResponseRedirect(reverse("watchlist", kwargs={'user':request.user}))
        #if in watchlist remove
        else:
            test.delete()
            return HttpResponseRedirect(reverse("watchlist", kwargs={'user':request.user}))
        #get request
    else:
        user = User.objects.get(username=request.user)
        watchlist = user.watchlist.all()
        return render(request, "auctions/watchlist.html",{
          "watchlists": user.watchlist.all()
        })
@login_required
def bid(request,title):
    user = request.user
    if request.method == "POST":
        user= request.user
        ls = Bid.objects.filter(listing_id =int(request.POST.get('id')))
        ls = ls.aggregate(Max('bids'))
        start = Listing.objects.get(pk=title)
        start = start.price
        #if no bids before
        if ls['bids__max'] is None:
            highest = start
            #if bid is higher or equal to the starting bid 
            if float(request.POST.get('bid')) >= highest:
                bid = Bid.objects.create(
                bids = request.POST.get('bid'),
                listing_id = Listing.objects.get(pk = int(request.POST.get('id'))),
                user_id= request.user
            )
                bid.save()
                return HttpResponseRedirect(reverse("indi", kwargs={'user':user,'title':title}))
            #not higher than starting bid, throws error
            else:
                return render(request,"auctions/error.html",{
                'message':"Bid must be higher than the starting bid!"
            })  
        #if have bid before, look for the highest bid
        else:
            highest = ls['bids__max']
            #if the current bid is higher than the highest bid,
            if float(request.POST.get('bid')) > highest:
                bid = Bid.objects.create(
                    bids = request.POST.get('bid'),
                    listing_id = Listing.objects.get(pk = int(request.POST.get('id'))),
                    user_id= request.user
                )
                bid.save()
                return HttpResponseRedirect(reverse("indi", kwargs={'user':user,'title':title}))
            #else throws error
            else:
                return render(request,"auctions/error.html",{
                'message':"Bid must be higher than the highest bid!"
            })
                
@login_required
def close(request,title):
    list = Listing.objects.get(pk=title)
    owner = list.user_id
    if request.user == owner:
        list.status = False
        bid = Bid.objects.filter(listing_id = list.id)
        #if no one bid for the item
        if not bid:
            return HttpResponseRedirect(reverse("inactive"))
        foo = bid.aggregate(Max('bids'))
        highest = foo['bids__max']
        bid = Bid.objects.get(bids = highest)
        list.winner = bid.user_id
        list.save()
        return HttpResponseRedirect(reverse("inactive"))

def category(request,cat):
    item = Category.objects.get(cat__iexact=cat)
    all = Listing.objects.filter(category = item, status=True)
    user = User.objects.all()
    cat = Category.objects.all()
    return render(request, "auctions/category.html",{
        "listing":all,
        'cat':cat,
        'current':item
    })