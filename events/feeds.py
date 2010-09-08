from django.contrib.auth.models import User
from django.core.urlresolvers import reverse
from django.contrib.sites.models import Site
from django.contrib.syndication.views import Feed, FeedDoesNotExist

from events.models import Event

current_site = Site.objects.get_current()

class BaseFeed(Feed):
	subtitle = u"More than a hapax legomenon."
	title_description = 'feeds/events_event_title.html'
	description_template = 'feeds/events_event_description.html'
	
	def item_pubdate(self, item):
		return item.published
	
	def item_updated(self, item):
		return item.date_modified
	
	def item_id(self, item):
		return item.get_absolute_url()
	
	def item_author_name(self, item):
		return u"%s %s" % (item.author.first_name, item.author.last_name)
	
	def item_author_email(self, item):
		return u"%s" % (item.author.email)
	
	def item_author_link(self, item):
		return reverse('events_index')
	
	def item_categories(self, item):
		return item.tags.all()
	
	def item_copyright(self, item):
		return u"Copyright (c) %s, %s %s" % (current_site.name, item.author.first_name, item.author.last_name)
	
	def feed_title(self):
		return u"%s" % current_site.name
	
	def feed_authors(self):
		return ({"name": user.name} for user in User.objects.filter(is_staff=True))

class EventsFeed(BaseFeed):
	title = u"%s: events calendar." % current_site.name
	
	def link(self):
		return reverse('events_index') + "?utm_source=feedreader&utm_medium=feed&utm_campaign=EventsFeed"
	
	def items(self):
		return Event.objects.published()[:10]
	
	def item_link(self, item):
		return item.get_absolute_url() + "?utm_source=feedreader&utm_medium=feed&utm_campaign=EventsFeed"