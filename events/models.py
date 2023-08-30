from django.db import models
from django.contrib.auth.models import User
from datetime import date


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=150)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)
    owner = models.IntegerField('Venue Owner', blank=False, default=1)
    venue_image = models.ImageField(null=True, blank=True, upload_to='images/')

    def __str__(self):
        return self.name


class Event(models.Model):
    name = models.CharField('Event name', max_length=150)
    event_data = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(User, blank=True, related_name='event_attendees')
    approved = models.BooleanField("Approved", default=False)

    def __str__(self):
        return self.name

    @property
    def days_till_event(self):
        today = date.today()
        if today > self.event_data.date():
            return 'Finished'

        elif today == self.event_data.date():
            event_time = self.event_data.time()
            return f"Today at: {event_time.strftime('%I:%M %p')}"

        date_time_till = self.event_data.date() - today
        days_till = str(date_time_till).split(',')[0]

        return days_till
