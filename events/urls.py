from django.urls import path
from . import views, download_views

urlpatterns = [
    path('', views.home, name="home"),
    path('<int:year>/<str:month>/', views.home, name="home"),
    path('Events', views.all_events, name="list-events"),
    path('add_venue', views.add_venue, name="add-venue"),
    path('list_venues', views.list_venues, name="list-venues"),
    path('show_venue/<venue_id>', views.show_venue, name="show-venue"),
    path('update_venue/<venue_id>', views.update_venue, name="update-venue"),
    path('update_event/<event_id>', views.update_event, name="update-event"),
    path('add_event', views.add_event, name="add-event"),
    path('delete_event/<event_id>', views.delete_event, name="delete-event"),
    path('delete_venue/<venue_id>', views.delete_venue, name="delete-venue"),
    path('all_venues_text', download_views.all_venues_text, name="all-venues-text"),
    path('venue_text/<venue_id>', download_views.venue_text, name="venue-text"),
    path('all_venues_csv', download_views.all_venues_csv, name="all-venues-csv"),
    path('venue_csv/<venue_id>', download_views.venue_csv, name="venue-csv"),
    path('all_venues_pdf', download_views.all_venues_pdf, name="all-venues-pdf"),
    path('venue_pdf/<venue_id>', download_views.venue_pdf, name="venue-pdf"),
    path('all_events_text', download_views.all_events_text, name="all-events-text"),
    path('event_text/<event_id>', download_views.event_text, name="event-text"),
    path('all_events_csv', download_views.all_events_csv, name="all-events-csv"),
    path('event_csv/<event_id>', download_views.event_csv, name="event-csv"),
    path('all_events_pdf', download_views.all_events_pdf, name="all-events-pdf"),
    path('event_pdf/<event_id>', download_views.event_pdf, name="event-pdf"),
    path('my_events', views.my_events, name="my-events"),
    path('show_event/<event_id>', views.show_event, name="show-event"),
    path('join_event/<event_id>', views.join_event, name="join-event"),
    path('leave_event/<event_id>', views.leave_event, name="leave-event"),
    path('admin_event_approval', views.admin_event_approval, name="admin-event-approval"),

]
