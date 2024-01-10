from django.contrib import admin
from .models import Listing, comment, Bid, Category, Picture

# Register your models here.

admin.site.register(Category)
admin.site.register(Listing)
admin.site.register(comment)
admin.site.register(Bid)
admin.site.register(Picture)