from django.test import Client
from django.core.urlresolvers import reverse

from events.models import Event
from tagging.models import Tag

from django.test import TestCase

client = Client()

class EventsTestCase(TestCase):
	fixtures = ['events',]
	
	def setUp(self):
		self.event = Event.objects.get(pk=3)
	
	def testEventsIndex(self):
		response = client.get(reverse('events_index'))
		self.assertEquals(response.status_code, 200)
	
	def testEventDetailThoughModel(self):
		response = client.get(self.event.get_absolute_url())
		self.assertEquals(response.status_code, 200)
	
	def testEventDetailThoughURL(self):
		year = self.event.published.year
		month = self.event.published.strftime('%b').lower()
		day = self.event.published.day
		slug = self.event.slug
		response = client.get(reverse('events_event_detail', args=[year, month, day, slug,]))
		self.assertEquals(response.status_code, 200)