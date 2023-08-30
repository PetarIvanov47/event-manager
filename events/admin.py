from django.contrib import admin
from .models import Venue
from .models import Event
from django.contrib.auth.models import Group

admin.site.unregister(Group)


@admin.register(Venue)
class VenueAdmin(admin.ModelAdmin):
    list_display = ('name', 'address', 'phone')
    ordering = ('name',)
    search_fields = ('name', 'address')


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    fields = (('name', 'venue'), 'event_data', 'description', 'manager', 'attendees', 'approved')
    list_display = ('name', 'event_data', 'venue')
    list_filter = ('event_data', 'venue')
    ordering = ('event_data',)




