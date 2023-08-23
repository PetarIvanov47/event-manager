from django.db import models
from django.contrib.auth.models import User


class Venue(models.Model):
    name = models.CharField('Venue Name', max_length=150)
    address = models.CharField(max_length=300)
    zip_code = models.CharField('Zip Code', max_length=15)
    phone = models.CharField('Contact Phone', max_length=25, blank=True)
    web = models.URLField('Website Address', blank=True)
    email_address = models.EmailField('Email Address', blank=True)

    def __str__(self):
        return self.name


class MyWebsiteUser(models.Model):
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    email = models.EmailField('User Email')

    def __str__(self):
        return f"{self.first_name} {self.last_name}"


class Event(models.Model):
    name = models.CharField('Event name', max_length=150)
    event_data = models.DateTimeField('Event Date')
    venue = models.ForeignKey(Venue, blank=True, null=True, on_delete=models.CASCADE)
    manager = models.ForeignKey(User, blank=True, null=True, on_delete=models.SET_NULL)
    description = models.TextField(blank=True)
    attendees = models.ManyToManyField(MyWebsiteUser, blank=True)

    def __str__(self):
        return self.name