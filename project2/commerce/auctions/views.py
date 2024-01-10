from django import forms
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.forms import ModelForm, modelformset_factory
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


from .models import Listing, User, Picture

class newListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'startingBid', 'category']
        widgets = {
            'title': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2'}),
            'description': forms.Textarea(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2','rows':'2'}),
            'startingBid': forms.NumberInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2'}),
            'category': forms.Select(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2'}),
        }


class newPictureForm(ModelForm):
    class Meta:
        model = Picture
        fields = ['picture', 'alt_text']
        widgets = {
            'picture': forms.FileInput(attrs={'class': 'block w-full text-sm text-gray-900 border border-gray-300 rounded-lg cursor-pointer bg-gray-50 dark:text-gray-400 focus:outline-none dark:bg-gray-700 dark:border-gray-600 dark:placeholder-gray-400',
                                               'type':'file'}),
            'alt_text': forms.TextInput(attrs={'class': 'w-full rounded-lg border border-gray-300 p-2'}),

        }

        
def index(request):
    return render(request, "auctions/index.html")


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
def newListing(request):
    PictureFormSet = modelformset_factory(Picture,
                                        form=newPictureForm, extra=3)
    if request.method == "POST":        
        form = newListingForm(request.POST, request.FILES)
        imagesForm = PictureFormSet(request.POST, request.FILES,
                               queryset=Picture.objects.none())
        if form.is_valid() and imagesForm.is_valid():
            newListing = form.save(commit=False)
            newListing.creator = request.user
            newListing.save()


            for form in imagesForm.cleaned_data:
                if form:
                    picture = form['picture']
                    text = 'image'
                    newPicture = Picture(listing=newListing, picture=picture, alt_text=text)
                    newPicture.save()

            return render(request, "auctions/newListing.html", {
                "form": newListingForm(),
                "imageForm": PictureFormSet(queryset=Picture.objects.none()),
                "success": True
        })
        else:
            return render(request, "auctions/newListing.html", {
                "form": newListingForm(),
                "imageForm": PictureFormSet(queryset=Picture.objects.none())
            })

    else:
        return render(request, "auctions/newListing.html", {
            "form": newListingForm(),
            "imageForm": PictureFormSet(queryset=Picture.objects.none())
        })
    
def listing(request, listing_id):
    return render(request, "auctions/listing.html")

"""path("auction/active", views.activeListings, name="activeListings"),
path("auction/active/<int:category_id>", views.activeListings, name="activeListings"),
path("auction/watchlist", views.watchlist, name="watchlist"),
path("auction/watchlist/<int:listing_id>/change/<str:reverse_method>", views.change_watchlist, name="change_watchlist"),
path("auction/listing/<int:listing_id>/bid", views.take_bid, name="take_bid"),    
path("auction/listing/<int:listing_id>/close", views.close_listing, name="close_listing"),
path("auction/listing/<int:listing_id>/comment", views.comment, name="comment")"""