from icalendar import Calendar, Event, vText, vUri

from django.contrib.sites.models import Site

def export_ical(events):
	cal = Calendar()
	
	site = Site.objects.get_current()
	
	cal.add('prodid', '-//%s Events Calendar//%s//' % (site.name, site.domain))
	cal.add('version', '2.0')
	
	site_token = site.domain.split('.')
	site_token.reverse()
	site_token = '.'.join(site_token)
	
	for event in events:
		ical_event = Event()
		ical_event.add('summary', event.title)
		ical_event.add('description', event.body)
		ical_event.add('dtstart', event.start_datetime)
		ical_event.add('dtend', event.end_datetime)
		ical_event.add('dtstamp', event.end_datetime)
		ical_event.add('url', vUri('http://' + site.domain + event.get_absolute_url()))
		ical_event['location'] = vText(event.location)
		ical_event['uid'] = '%d.event.events.%s' % (event.id, site_token)
		cal.add_component(ical_event)
	
	return cal