from django.contrib.sitemaps import Sitemap

from events.models import Event

class EventsSitemap(Sitemap):
	changefreq = "never"
	priority = 1.0
	
	def items(self):
		return Event.objects.public()
	
	def lastmod(self, obj):
		return obj.date_modified