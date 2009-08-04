import djapian

from asgard.calendar.models import Event

class EventIndexer(djapian.Indexer):
	fields = [
		'title',
		'body',
		'tags',
	]
	
	tags = [
		('title', 'title', 2),
		('body', 'body', 1),
		('tag', 'tags', 1)
	]

djapian.add_index(Event, EventIndexer, attach_as="indexer")