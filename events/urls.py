from django.urls import path
from . import views, downloads

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('Events', views.all_events, name="list-events"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('list_venues', views.list_venues, name="list-venues"),
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"),
    path('search_venues', views.search_venues, name="search-venues"),
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('add_event', views.add_event, name="add-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('all_venues_text', downloads.all_venues_text, name="all-venues-text"),
    path('venue_text/<venue_id>', downloads.venue_text, name="venue-text"),
    path('all_venues_csv', downloads.all_venues_csv, name="all-venues-csv"),
    path('venue_csv/<venue_id>', downloads.venue_csv, name="venue-csv"),
    path('all_venues_pdf', downloads.all_venues_pdf, name="all-venues-pdf"),
    path('venue_pdf/<venue_id>', downloads.venue_pdf, name="venue-pdf"),
    path('all_events_text', downloads.all_events_text, name="all-events-text"),
    path('event_text/<event_id>', downloads.event_text, name="event-text"),
    path('all_events_csv', downloads.all_events_csv, name="all-events-csv"),
    path('event_csv/<event_id>', downloads.event_csv, name="event-csv"),
    path('all_events_pdf', downloads.all_events_pdf, name="all-events-pdf"),
    path('event_pdf/<event_id>', downloads.event_pdf, name="event-pdf"),

]
