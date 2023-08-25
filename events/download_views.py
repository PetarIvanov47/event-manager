import csv
from django.http import FileResponse
from .models import Venue, Event
from django.http import HttpResponse
import csv
import io
from reportlab.pdfgen import canvas
from reportlab.lib.units import inch
from reportlab.lib.pagesizes import letter


# Venue Files

# Generate Text File For Single Venue
def venue_text(request, venue_id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venue.txt'

    venue = Venue.objects.get(pk=venue_id)

    lines = [f'VENUE INFO:\n\n',
             f'Name - {venue.name}\n',
             f'Address - {venue.address}\n',
             f'Zip Code - {venue.zip_code}\n',
             f'Phone - {venue.phone}\n',
             f'Web Address - {venue.web}\n',
             f'Email Address - {venue.email_address}\n\n\n'
             ]

    response.writelines(lines)
    return response


# Generate Text File Venue List
def all_venues_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=venues.txt'

    venues = Venue.objects.all()

    lines = ['VENUES INFO:\n\n']
    for venue in venues:
        lines.append(f'Name - {venue.name}\n'
                     f'Address - {venue.address}\n'
                     f'Zip Code - {venue.zip_code}\n'
                     f'Phone - {venue.phone}\n'
                     f'Web Address - {venue.web}\n'
                     f'Email Address - {venue.email_address}\n\n\n'
                     )

    response.writelines(lines)
    return response


# Generate Csv File Venue List
def all_venues_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venues.csv'

    # Create a csv writer
    writer = csv.writer(response)

    venues = Venue.objects.all()

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email Address'])

    for venue in venues:
        writer.writerow([venue.name,
                         venue.address,
                         venue.zip_code,
                         venue.phone,
                         venue.web,
                         venue.email_address]
                        )

    return response


# Generate Csv File For Single Venue
def venue_csv(request, venue_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=venue.csv'

    # Create a csv writer
    writer = csv.writer(response)

    venue = Venue.objects.get(pk=venue_id)

    # Add column headings to the csv file
    writer.writerow(['Venue Name', 'Address', 'Zip Code', 'Phone', 'Web Address', 'Email Address'])

    writer.writerow([venue.name,
                     venue.address,
                     venue.zip_code,
                     venue.phone,
                     venue.web,
                     venue.email_address]
                    )

    return response


# Generate PDF File Venue List
def all_venues_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 14)

    venues = Venue.objects.all()

    lines = []

    for venue in venues:
        lines.append(f"Name - {venue.name}")
        lines.append(f"Address - {venue.address}")
        lines.append(f"Zip Code - {venue.zip_code}")
        lines.append(f"Phone - {venue.phone}")
        lines.append(f"Web Address - {venue.web}")
        lines.append(f"Email Address - {venue.email_address}")
        lines.append("=" * 50)

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venues.pdf')


# Generate PDF File For Single Venue
def venue_pdf(request, venue_id):
    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 15)

    venue = Venue.objects.get(pk=venue_id)

    lines = [f"Name - {venue.name}",
             f"Address - {venue.address}",
             f"Zip Code - {venue.zip_code}",
             f"Phone - {venue.phone}",
             f"Web Address - {venue.web}",
             f"Email Address - {venue.email_address}",
             ]

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='venue.pdf')


# Events Files

# Generate Text File For Single Event
def event_text(request, event_id):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=event.txt'

    event = Event.objects.get(pk=event_id)

    lines = [f'EVENT INFO:\n\n',
             f'Name - {event.name}\n',
             f'Date - {event.event_data}\n',
             f'Venue - {event.venue}\n',
             f'Manager - {event.manager}\n',
             f'Description - {event.description}\n',
             f'Attendees - {", ".join(str(a) for a in event.attendees.all())}\n\n\n'
             ]

    response.writelines(lines)
    return response


# Generate Text File Events List
def all_events_text(request):
    response = HttpResponse(content_type='text/plain')
    response['Content-Disposition'] = 'attachment; filename=events.txt'

    events = Event.objects.all().order_by('event_data', 'name')

    lines = ['EVENTS INFO:\n\n']
    for event in events:
        lines.append(f'Name - {event.name}\n'
                     f'Date - {event.event_data}\n'
                     f'Venue - {event.venue}\n'
                     f'Manager - {event.manager}\n'
                     f'Description - {event.description}\n'
                     f'Attendees - {", ".join(str(a) for a in event.attendees.all())}\n\n\n'
                     )

    response.writelines(lines)
    return response


# Generate Csv File Events List
def all_events_csv(request):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=events.csv'

    # Create a csv writer
    writer = csv.writer(response)

    events = Event.objects.all().order_by('event_data', 'name')

    # Add column headings to the csv file
    writer.writerow(['Event Name', 'Event Date', 'Venue', 'Manager', 'Description', 'Attendees'])

    for event in events:

        writer.writerow([event.name,
                         event.event_data,
                         event.venue,
                         event.manager,
                         event.description, ", ".join(str(a) for a in event.attendees.all())])

    return response


# Generate Csv File For Single Event
def event_csv(request, event_id):
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename=event.csv'

    # Create a csv writer
    writer = csv.writer(response)

    event = Event.objects.get(pk=event_id)

    # Add column headings to the csv file
    writer.writerow(['Event Name', 'Event Date', 'Venue', 'Manager', 'Description', 'Attendees'])

    writer.writerow([event.name,
                     event.event_data,
                     event.venue,
                     event.manager,
                     event.description,
                     ", ".join(str(a) for a in event.attendees.all())]
                    )

    return response


# Generate PDF File Events List
def all_events_pdf(request):
    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 14)

    events = Event.objects.all().order_by('event_data', 'name')

    lines = []

    for event in events:
        lines.append(f"Name - {event.name}")
        lines.append(f"Event Date - {event.event_data}")
        lines.append(f"Venue - {event.venue}")
        lines.append(f"Manager - {event.manager}")
        lines.append(f"Description - {event.description}")
        lines.append(f"Attendees - {', '.join(str(a) for a in event.attendees.all())}")
        lines.append("=" * 50)

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='events.pdf')


# Generate PDF File For Single Event
def event_pdf(request, event_id):
    # Create Bytestream buffer
    buf = io.BytesIO()

    # Create a canvas
    c = canvas.Canvas(buf, pagesize=letter, bottomup=0)

    # Create a text object
    text_obj = c.beginText()
    text_obj.setTextOrigin(inch, inch)
    text_obj.setFont("Helvetica", 15)

    event = Event.objects.get(pk=event_id)

    lines = [f"Name - {event.name}",
             f"Event Date - {event.event_data}",
             f"Venue - {event.venue}",
             f"Manager - {event.manager}",
             f"Description - {event.description}",
             f"Attendees - {', '.join(str(a) for a in event.attendees.all())}",
             ]

    for line in lines:
        text_obj.textLine(line)

    c.drawText(text_obj)
    c.showPage()
    c.save()
    buf.seek(0)

    return FileResponse(buf, as_attachment=True, filename='event.pdf')