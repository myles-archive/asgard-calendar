from django.conf.urls.defaults import *

from events.feeds import EventsFeed

urlpatterns = patterns('',
	url(r'feed/$',
		view = EventsFeed(),
		name = 'events_feed'
	)
)

urlpatterns += patterns('events.views',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
		view = 'detail',
		name = 'events_event_detail',
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
		view = 'events_day',
		name = 'events_day',
	),
	url(r'^(?P<year>\d{4})/(?P<week>[0-9]{2})/$',
		view = 'events_week',
		name = 'events_week'
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
		view = 'events_month',
		name = 'events_month',
	),
	url(r'^(?P<year>\d{4})/$',
		view = 'events_year',
		name = 'events_year',
	),
	url(r'^archive/$',
		view = 'events_archives',
		name = 'events_archives'
	),
	url(r'^today/$',
	    view = 'events_day',
	    name = 'events_today'
	),
	url(r'^$',
		view = 'events_month',
		name = 'events_index',
	),
)