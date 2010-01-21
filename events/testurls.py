from django.conf.urls.defaults import patterns, url, include
from django.contrib import admin

from events.sitemaps import CalendarEventSitemap
# from events.feeds import 

admin.autodiscover()

feeds = {}

sitemaps = {}

urlpatterns = patterns('',
	(r'^admin/', include(admin.site.urls)),
	(r'^comments/', include('django.contrib.comments.urls')),
	
	(r'^calendar/', include('events.urls')),
	
	(r'^locations/', include('asgard.locations.urls')),
	
	url(r'^feeds/(?P<url>.*)/$',
		'django.contrib.syndication.views.feed',
		{ 'feed_dict': feeds },
		name = 'feeds'
	),
	
	url(r'^sitemap.xml$',
		'django.contrib.sitemaps.views.sitemap',
		{ 'sitemaps': sitemaps },
		name = 'sitemap'
	),
)