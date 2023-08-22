from django.shortcuts import render, redirect
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from .models import Event, Venue
from .forms import VenueForm, EventForm
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator


def delete_venue(request, venue_id):
    venue = Venue.objects.get(pk=venue_id)

    if request.method == "POST":
        venue.delete()
        return redirect('list-venues')

    return render(request, 'events/delete_venue.html', {'venue': venue})


def delete_event(request, event_id):
    event = Event.objects.get(pk=event_id)

    if request.method == "POST":
        event.delete()
        return redirect('list-events')

    return render(request, 'events/delete_event.html', {'event': event})


def update_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    form = EventForm(request.POST or None, instance=event)
    if form.is_valid():
        form.save()
        return redirect('list-events')

    return render(request, 'events/update_event.html', {'event': event, 'form': form})


def add_event(request):
    submitted = False

    if request.method == "POST":
        form = EventForm(request.POST)

        if form.is_valid():
            form.save()
            return HttpResponseRedirect('/add_event?submitted=True')

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
        return redirect('list-venues')

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
    return render(request, 'events/show_venue.html', {'venue': venue})


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
            form.save()
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
