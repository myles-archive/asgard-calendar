from dateutil.relativedelta import relativedelta
import datetime

from django.db import models
from django.db.models import permalink
from django.contrib.auth.models import User
from django.contrib.contenttypes import generic
from django.contrib.comments.models import Comment
from django.utils.translation import ugettext_lazy as _

from taggit.managers import TaggableManager

from events.managers import EventManager

from asgard.utils.db.fields import MarkupTextField

class Event(models.Model):
	title = models.CharField(_('title'), max_length=200)
	slug = models.SlugField(_('slug'), max_length=25)
	author = models.ForeignKey(User)
	
	start_date = models.DateField(_('start date'))
	start_time = models.TimeField(_('start time'), blank=True, null=True)
	end_date = models.DateField(_('end date'), blank=True, null=True)
	end_time = models.TimeField(_('end time'), blank=True, null=True)
	cancel = models.BooleanField(_('cancel'), default=False)
	
	location = models.TextField(_('location'), blank=True, null=True)
	
	allow_comments = models.BooleanField(_('allow comments'), default=True)
	
	tags = TaggableManager()
	
	body = MarkupTextField(_('body'))
	
	published = models.DateTimeField(_('published'), blank=True, null=True)
	date_added = models.DateTimeField(_('date added'), auto_now_add=True)
	date_modified = models.DateTimeField(_('date modified'), auto_now=True)
	
	private = models.BooleanField(_('Private'), default=False)
	
	comments = generic.GenericRelation(Comment, object_id_field='object_pk')
	
	objects = EventManager()
	
	class Meta:
		verbose_name = _('event')
		verbose_name_plural = _('events')
		db_table = 'events'
		unique_together = ('slug', 'start_date',)
		ordering = ('-start_date', '-start_time')
	
	def __unicode__(self):
		return u"%s" % self.title
	
	@permalink
	def get_absolute_url(self):
		return ('events_event_detail', None, {
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
			return datetime.datetime.combine(self.start_date,
				datetime.time(0, 0))
	
	@property
	def end_datetime(self):
		if self.end_time and self.end_date:
			return datetime.datetime.combine(self.end_date, self.end_time)
		elif not self.end_date:
			return datetime.datetime.combine(self.start_date,
				self.end_time)
		elif not self.end_time and self.end_date:
			return datetime.datetime.combine(self.end_date,
				datetime.time(0, 0))
		else:
			return datetime.datetime.combine(self.start_date,
				datetime.time(0, 0))
	
	@property
	def length(self):
		if self.end_date:
			length = relativedelta(self.end_date, self.start_date)
		elif self.start_time and self.end_time:
			length = relativedelta(
				datetime.datetime.combine(self.start_date, self.end_time),
				datetime.datetime.combine(self.start_date, self.start_time))
		elif self.end_date and self.start_time:
			length = relativedelta(
				datetime.datetime.combine(self.end_date, self.start_time),
				datetime.datetime.combine(self.start_date, self.start_time))
		elif self.end_date and self.end_time:
			length = relativedelta(
				datetime.datetime.combine(self.end_date, self.end_time),
				datetime.datetime.combine(self.start_date, self.end_time))
		else:
			return None
		
		return u"%s:%s" % (length.hours, length.minutes)
	
	def _get_tags(self):
		tag_string = ''
		for t in self.tags.all():
			link = '<a href="./?tags__id__exact=%s" title="Show all post under %s tag">%s</a>' % (t.slug, t.name, t.name)
			link = u"%s" % t.name
			tag_string = ''.join([tag_string, link, ', '])
		return tag_string.rstrip(', ')
	
	_get_tags.short_description = _('Tags')
	_get_tags.allow_tags = True