from django.contrib import admin

from .models import House

class HouseAdmin(admin.ModelAdmin):
    list_display = ('id','created_on')
    # search_fields = ('address', 'description')
    # list_filter = ('created_on', 'manager')


admin.site.register(House, HouseAdmin)
# Register your models here.
