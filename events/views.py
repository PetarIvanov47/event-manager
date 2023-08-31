from django.shortcuts import render, redirect
from django.contrib import messages
import calendar
from calendar import HTMLCalendar
from datetime import datetime, date
from .models import Event, Venue
from django.contrib.auth.models import User
from .forms import VenueForm, EventForm, EventFormAdmin
from django.http import HttpResponseRedirect
from django.core.paginator import Paginator
from django.db.models import Q


# Admin Event Approval Page
def admin_panel(request):
    # MyClub Stats
    event_count = Event.objects.all().count
    venue_count = Venue.objects.all().count
    user_count = User.objects.all().count

    # New events for approval
    new_events = Event.objects.filter(approved=False).order_by('event_data')

    # Past Events For Clear
    today = date.today()
    past_events = Event.objects.filter(event_data__lt=today)

    if request.user.is_superuser:

        # Posting In Page
        if request.method == "POST":
            if "approve_events" in request.POST:
                id_list = request.POST.getlist('boxes')
                [Event.objects.filter(pk=int(x)).update(approved=True) for x in id_list]

                messages.success(request, "Events Approved!")
                return redirect('home')

            elif "clear_events" in request.POST:
                past_events.delete()
                messages.success(request, "Successfully Deleted Past Events!")
                return redirect('home')

        # Just Getting The Page
        else:
            return render(request, 'events/admin_event_approval.html', {'new_events': new_events,
                                                                        'past_events': past_events,
                                                                        'event_count': event_count,
                                                                        'venue_count': venue_count,
                                                                        'user_count': user_count
                                                                        }
                          )
    # If Someone Who Is Not SuperUser Trying To View The Page
    else:
        messages.success(request, "You aren't authorized to view this page!")
        return redirect('home')


# Leave Event
def leave_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        if request.user in event.attendees.all():
            event.attendees.remove(request.user)
            messages.success(request, f"{request.user} Successfully Leave The Event - {event}")
            return redirect(request.META['HTTP_REFERER'])

        else:
            messages.success(request, f"{request.user} Is Not Registered For - {event}!")
            return redirect(request.META['HTTP_REFERER'])

    else:
        return redirect('login')


# Join Event
def join_event(request, event_id):
    if request.user.is_authenticated:
        event = Event.objects.get(pk=event_id)
        if request.user in event.attendees.all():
            messages.success(request, f"{request.user} Is Register For This Event!")
            return redirect(request.META['HTTP_REFERER'])

        event.attendees.add(request.user)
        messages.success(request, f"{request.user} Successfully Join Event - {event}!")
        return redirect(request.META['HTTP_REFERER'])

    else:
        return redirect('login')


# Set up Pagination
def set_paginator(request, obj, pages: int):
    p = Paginator(obj, pages)
    page = request.GET.get('page')
    return p.get_page(page)


def my_events(request):
    if request.user.is_authenticated:
        me = request.user.id
        list_events = Event.objects.filter(attendees=me, approved=True).order_by('event_data', 'name')
        events = set_paginator(request, list_events, 5)

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
                form.save_m2m()
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
    form = VenueForm(request.POST or None, request.FILES or None, instance=venue)
    if form.is_valid():
        form.save()
        messages.success(request, f'You Successfully Updated Venue - "{venue.name}"')

        return redirect("show-venue", venue_id=venue_id)

    return render(request, 'events/update_venue.html', {'venue': venue, 'form': form})


def show_venue(request, venue_id):
    # Get Venue Object
    venue = Venue.objects.get(pk=venue_id)

    # Get Venue Object Owner
    venue_owner = User.objects.get(pk=venue.owner)

    # Get Events At This Venue
    event_list = venue.event_set.all()

    return render(request, 'events/show_venue.html', {'venue': venue,
                                                      'venue_owner': venue_owner,
                                                      'event_list': event_list}
                  )

def list_venues(request):
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        venues = Venue.objects.filter(name__contains=searched).order_by('name')
        all_venues = set_paginator(request, venues, 5)

        return render(request, 'events/venue.html', {'all_venues': all_venues, 'searched': searched})

    else:
        venues = Venue.objects.all().order_by('name')
        all_venues = set_paginator(request, venues, 5)
        return render(request, 'events/venue.html', {'all_venues': all_venues})


def add_venue(request):
    submitted = False

    if request.method == "POST":
        form = VenueForm(request.POST, request.FILES)

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
    if request.method == "POST":
        searched = request.POST.get('searched', '')
        events = Event.objects.filter(
            Q(name__icontains=searched) |
            Q(manager__username__icontains=searched) |
            Q(venue__name__icontains=searched),
            approved=True
        ).order_by('event_data',
                   'name')

        event_list = set_paginator(request, events, 5)

        return render(request,
                      'events/event_list.html',
                      {'event_list': event_list,
                       'searched': searched}
                      )

    else:
        events = Event.objects.filter(approved=True).order_by('event_data', 'name')
        event_list = set_paginator(request, events, 5)
        return render(request, 'events/event_list.html', {'event_list': event_list})


def show_event(request, event_id):
    event = Event.objects.get(pk=event_id)
    return render(request, 'events/show_event.html', {'event': event})


def search_month_events(request):
    pass


def home(request, year=datetime.now().year, month=datetime.now().strftime('%B')):

    if request.user.is_authenticated:
        month = month.title()
        month_number = list(calendar.month_name).index(month)
        month_number = int(month_number)

        cal = HTMLCalendar().formatmonth(year, month_number)

        now = datetime.now()
        current_year = now.year

        event_list = Event.objects.filter(
            event_data__year=year,
            event_data__month=month_number,
            approved=True
        ).order_by('event_data', 'name')

        time = now.strftime('%I:%M:%S %p')
        return render(request,
                      'events/home.html',
                      {'year': year,
                       'month': month,
                       'month_number': month_number,
                       'cal': cal,
                       'current_year': current_year,
                       'time': time,
                       'event_list': event_list,
                       })
    else:
        return redirect('login')
