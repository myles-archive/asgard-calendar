from django.contrib import admin

from events.models import Event

class EventAdmin(admin.ModelAdmin):
	list_display = ('title', 'start_date', 'published', '_get_tags')
	date_hierarchy = 'start_date'
	search_field = ('title',)

admin.site.register(Event, EventAdmin)