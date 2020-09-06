from django.contrib import admin
from .models import *
from import_export.admin import ImportExportModelAdmin

# Register your odels here.

admin.site.register([City,Blog,Siteinformation,LocationGuider,Reply])

                    
@admin.register(LocationCategory)
class LocationCategory(ImportExportModelAdmin):
    pass

@admin.register(Location)
class Location(ImportExportModelAdmin):
    pass 

@admin.register(LocationReview)
class LocationReview(ImportExportModelAdmin):
    pass

@admin.register(Visitor)
class Visitor(ImportExportModelAdmin):
    pass