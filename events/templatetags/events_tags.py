import re

from django import template
from django.conf import settings
from django.db import models

Bookmark = models.get_model('events', 'event')

register = template.Library()

class UpcomingEvents(template.Node):
	"""
	Get a list of upcoming events.
	"""
	def __init__(self, limit, var_name):
		self.limit = limit
		self.var_name = var_name
	
	def render(self, context):
		events = Event.objects.upcoming()[:int(self.limit)]
		
		if (int(self.limit) == 1):
			context[self.var_name] = events[0]
		else:
			context[self.var_name] = events
		
		return ''

@register.tag
def get_upcoming_events(parser, token):
	"""
	Gets any number of upcoming events and stores them in a varable.

	Syntax::

		{% get_upcoming_events [limit] as [var_name] %}

	Example usage::

		{% get_upcoming_events 10 as upcoming_event_list %}
	"""
	try:
		tag_name, arg = token.contents.split(None, 1)
	except ValueError:
		raise template.TeamplteSyntaxError, "%s tag requires arguments" % token.contents.split()[0]

	m = re.search(r'(.*?) as (\w+)', arg)

	if not m:
		raise template.TemplateSyntaxError, "%s tag had invalid arguments" % tag_name

	format_string, var_name = m.groups()

	return UpcomingEvents(format_string[0], var_name)
