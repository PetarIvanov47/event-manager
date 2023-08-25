from django.shortcuts import render, redirect
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        events = Event.objects.filter(attendees=me)

        return render(request, 'events/my_events.html', {'events': events})
    else:
        messages.success(request, f"You aren't Authorized To View This Page!")
        return redirect('home')


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    if request.method == "POST":
        venue.delete()
        messages.success(request, f'Successfully Deleted Venue - "{venue.name}"')
        return redirect('list-venues')

    return render(request, 'events/delete_venue.html', {'venue': venue})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)

    if request.method == "POST":
        event.delete()
        messages.success(request, f'Successfully Deleted Event - "{event.name}"')
        return redirect('list-events')

    return render(request, 'events/delete_event.html', {'event': event})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    if request.user.is_superuser:
        form = EventFormAdmin(request.POST or None, instance=event)
    else:
        form = EventForm(request.POST or None, instance=event)

    if form.is_valid():
        form.save()
        messages.success(request, f'You Successfully Update Event - "{event.name}"')
        return redirect('list-events')

    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def add_event(request):
    submitted = False

    if request.method == "POST":
        if request.user.is_superuser:
            form = EventFormAdmin(request.POST)
            if form.is_valid():
                form.save()
                return HttpResponseRedirect('/add_event?submitted=True')

        else:
            form = EventForm(request.POST)
            if form.is_valid():
                event = form.save(commit=False)
                event.manager = request.user
                event.save()
                return HttpResponseRedirect('/add_event?submitted=True')

    else:
        # Just going to the page, not submitting
        if request.user.is_superuser:
            form = EventFormAdmin

        else:
            form = EventForm

        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_event.html', {'form': form, 'submitted': submitted})


def update_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    form = VenueForm(request.POST or None, instance=venue)
    if form.is_valid():
        form.save()
        messages.success(request, f'You Successfully Update Venue - "{venue.name}"')

        return redirect("show-venue", venue_id=venue_id)

    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def search_venues(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        venues = Venue.objects.filter(name__contains=searched).order_by('name')

        return render(request, 'events/search_venues.html', {'searched': searched, 'venues': venues})

    else:
        return render(request, 'events/search_venues.html', {})


def show_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)
    venue_owner = User.objects.get(pk=venue.owner)
    return render(request, 'events/show_venue.html', {'venue': venue, 'venue_owner': venue_owner})


def list_venues(request):
    # Set up Pagination
    p = Paginator(Venue.objects.all().order_by('name'), 5)
    page = request.GET.get('page')
    venues = p.get_page(page)
    return render(request, 'events/venue.html', {'venues': venues})


def add_venue(request):
    submitted = False

    if request.method == "POST":
        form = VenueForm(request.POST)

        if form.is_valid():
            venue = form.save(commit=False)
            venue.owner = request.user.id
            venue.save()
            # form.save()
            return HttpResponseRedirect('/add_venue?submitted=True')

    else:
        form = VenueForm
        if 'submitted' in request.GET:
            submitted = True

    return render(request, 'events/add_venue.html', {'form': form, 'submitted': submitted})


def all_events(request):
    # Set up Pagination
    p = Paginator(Event.objects.all().order_by('event_data', 'name'), 5)
    page = request.GET.get('page')
    event_list = p.get_page(page)
    return render(request, 'events/event_list.html', {'event_list': event_list})


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):
    name = "Petur"
    month = month.title()
    month_number = list(calendar.month_name).index(month)
    month_number = int(month_number)

    cal = HTMLCalendar().formatmonth(year, month_number)

    now = datetime.now()
    current_year = now.year

    time = now.strftime('%I:%M:%S %p')
    return render(request,
                  'events/home.html',
                  {'name': name,
                   'year': year,
                   'month': month,
                   'month_number': month_number,
                   'cal': cal,
                   'current_year': current_year,
                   'time': time,
                   })
