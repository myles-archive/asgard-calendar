"""
Copyright (C) 2008 Myles Braithwaite

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at
	
	http://www.apache.org/licenses/LICENSE-2.0
	
Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.
"""

from django.conf.urls.defaults import *

urlpatterns = patterns('asgard.calendar.views',
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/(?P<slug>[-\w]+)/$',
		view = 'detail',
		name = 'calendar_event_detail',
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/(?P<day>\w{1,2})/$', 
		view = 'calendar_day',
		name = 'calendar_day',
	),
	url(r'^(?P<year>\d{4})/(?P<week>[1-9]{2})/$',
		view = 'calendar_week',
		name = 'calendar_week'
	),
	url(r'^(?P<year>\d{4})/(?P<month>[a-z]{3})/$',
		view = 'calendar_month',
		name = 'calendar_month',
	),
	url(r'^(?P<year>\d{4})/$',
		view = 'calendar_month',
		name = 'calendar_year',
	),
	url(r'^today/$',
	    view = 'calendar_day',
	    name = 'calendar_today'
	),
	url(r'^calendar\.ics$',
		view = 'icalendar',
		name = 'calendar_ics'
	),
	url(r'^$',
		view = 'calendar_month',
		name = 'calendar_index',
	),
)
