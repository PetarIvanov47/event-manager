from django.contrib import admin
from .models import Venue
from .models import MyWebsiteUser
from .models import Event

# admin.site.register(Venue)
admin.site.register(MyWebsiteUser)
# admin.site.register(Event)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_data', 'description', 'manager', 'attendees')
    list_display = ('name', 'event_data', 'venue')
    list_filter = ('event_data', 'venue')
    ordering = ('event_data',)

