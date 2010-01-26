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
		year = self.event.start_date.year
		month = self.event.start_date.strftime('%b').lower()
		day = self.event.start_date.day
		slug = self.event.slug
		response = client.get(reverse('events_event_detail', args=[year, month, day, slug,]))
		self.assertEquals(response.status_code, 200)
	
	def testEventYear(self):
		year = self.event.start_date.year
		response = client.get(reverse('events_year', args=[year,]))
		self.assertEquals(response.status_code, 200)
	
	def testEventMonth(self):
		year = self.event.start_date.year
		month = self.event.start_date.strftime('%b').lower()
		response = client.get(reverse('events_month', args=[year, month,]))
		self.assertEquals(response.status_code, 200)
	
	def testEventDay(self):
		year = self.event.start_date.year
		month = self.event.start_date.strftime('%b').lower()
		day = self.event.start_date.day
		response = client.get(reverse('events_day', args=[year, month, day]))
		self.assertEquals(response.status_code, 200)
	
	def testEventsSitemap(self):
		response = client.get(reverse('sitemap'))
		self.assertEquals(response.status_code, 200)
	
	def testEventsEventFeed(self):
		response = client.get(reverse('feeds', args=['calendar']))
		self.assertEquals(response.status_code, 200)
