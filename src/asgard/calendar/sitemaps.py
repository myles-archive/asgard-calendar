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

from django.contrib.sitemaps import Sitemap

from asgard.calendar.models import Event

class EventSitemap(Sitemap):
	changefreq = "never"
	priority = 1.0
	
	def items(self):
		return Event.objects.all()
	
	def lastmod(self, obj):
		return obj.date_modified
