from django.contrib import admin
from .models import *

# Register your models here.

admin.site.register([City, LocationCategory, Location,
                      Blog,LocationReview,Siteinformation,LocationGuider,Visitor,Reply])

