from django.contrib import admin

from asgard.calendars.models import Event

class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'published')
	date_hierarchy = 'start_date'
	search_field = ('title',)

admin.site.register(Event, EventAdmin)