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

from dateutil.relativedelta import relativedelta
import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _
from django.db.models.signals import post_save, post_delete

from asgard.calendar.managers import EventManager
from asgard.related.models import RelatedLink, RelatedObject
from asgard.utils.db.fields import MarkupTextField
from asgard.tags import register as tags_register
from asgard.tags.fields import TagField
from asgard.tumblelog.signals import *
from asgard.locations.models import Location

class Event(models.Model):
	title = models.CharField(_('title'), max_length=200)
	slug = models.SlugField(_('slug'), max_length=25)
	
	start_date = models.DateField(_('start date'))
	start_time = models.TimeField(_('start time'), blank=True, null=True)
	end_date = models.DateField(_('end date'), blank=True, null=True)
	end_time = models.TimeField(_('end time'), blank=True, null=True)
	cancel = models.BooleanField(_('cancel'), default=False)
	
	location = models.ForeignKey(Location, verbose_name='Location', blank=True, null=True)
	
	allow_comments = models.BooleanField(_('Allow Comments'), default=True)
	
	tags = TagField()
	
	body = MarkupTextField(_('body'))
	
	published = models.DateTimeField(_('published'), blank=True, null=True)
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	private = models.BooleanField(_('Private'), default=False)
	
	comments = generic.GenericRelation(Comment, object_id_field='object_pk')
	related_links = generic.GenericRelation(RelatedLink)
	related_objects = generic.GenericRelation(RelatedObject)
	
	objects = EventManager()
	
	class Meta:
		verbose_name = _('event')
		verbose_name_plural = _('events')
		db_table = 'calendar_events'
		unique_together = ('slug', 'start_date',)
		ordering = ('-start_date', '-start_time')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('calendar_event_detail', None, {
			'slug':	self.slug,
			'year': self.start_date.year,
			'month': self.start_date.strftime('%b').lower(),
			'day': self.start_date.day,
		})
	
	@property
	def start_datetime(self):
		if self.start_time:
			return datetime.datetime.combine(self.start_date, self.start_time)
		else:
			return datetime.datetime.combine(self.start_date, datetime.time(0, 0))
	
	@property
	def end_datetime(self):
		if self.end_time and self.end_date:
			return datetime.datetime.combine(self.end_date, self.end_time)
		elif not self.end_date:
			return datetime.datetime.combine(self.start_date, self.end_time)
		elif not self.end_time and self.end_date:
			return datetime.datetime.combine(self.end_date, datetime.time(0, 0))
		else:
			return datetime.datetime.combine(self.start_date, datetime.time(0, 0))
	
	@property
	def length(self):
		if self.end_date:
			length = relativedelta(self.end_date, self.start_date)
		elif self.start_time and self.end_time:
			length = relativedelta(datetime.datetime.combine(self.start_date, self.end_time), datetime.datetime.combine(self.start_date, self.start_time))
		elif self.end_date and self.start_time:
			length = relativedelta(datetime.datetime.combine(self.end_date, self.start_time), datetime.datetime.combine(self.start_date, self.start_time))
		elif self.end_date and self.end_time:
			length = relativedelta(datetime.datetime.combine(self.end_date, self.end_time), datetime.datetime.combine(self.start_date, self.end_time))
		else:
			return None
		
		return u"%s.%s" % (length.hours, ((length.minutes * 100) / 60))

tags_register(Event, 'tag_set')
post_save.connect(add_modified_tumblelog_signal, sender=Event)
post_delete.connect(delete_tumblelog_signal, sender=Event)