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

from django.contrib import admin

from asgard.calendar.models import Event
from asgard.related.admin import RelatedLinkInline, RelatedObjectInline

class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'published')
	date_hierarchy = 'start_date'
	search_field = ('title',)
	inlines = [
		RelatedLinkInline,
		RelatedObjectInline,
	]

admin.site.register(Event, EventAdmin)