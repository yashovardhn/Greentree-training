from django.contrib import admin

from .models import House

class HouseAdmin(admin.ModelAdmin):
    list_display = ('name','id','created_on','manager','points')
    # Enable a better widget for selecting members
    filter_vertical = ('members',)  # Adds a dual-list widget for members
    # search_fields = ('address', 'description')
    # list_filter = ('created_on', 'manager')


admin.site.register(House, HouseAdmin)
# Register your models here.
