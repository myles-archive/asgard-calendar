import datetime
import time

from django.template import RequestContext
from django.http import Http404, HttpResponse
from django.shortcuts import render_to_response
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from events.models import Event
from events.forms import CalendarYearMonthForm
from events.utils import export_ical

def events_month(request, year=None, month=None):
	if not year:
		year = str(datetime.date.today().year)
	
	if not month:
		month = datetime.date.today().strftime('%b').lower()
	
	if request.GET:
		new_data = request.GET.copy()
		form = CalendarYearMonthForm(new_data)
		if form.is_valid():
			if form.cleaned_data['year']:
				year = str(form.cleaned_data['year'])
			else:
				year = str(datetime.date.today().year)
			if form.cleaned_data['month']:
				month = form.cleaned_data['month']
	
	try:
		month = datetime.date(*time.strptime(year+month, '%Y%b')[:3])
	except ValueError:
		raise Http404
	
	if month == datetime.date.today():
		today = True
	else:
		today = False
	
	# Had some issuse with time past 1000.
	if int(year) <= 1000:
		raise Http404
	
	# Had some issue with time later than 9999.
	if int(year) >= 9999:
		raise Http404
	
	event_list = Event.objects.filter(start_date__year=month.year, start_date__month=month.month)
	
	first_day = month.replace(day=1)
	if first_day.month == 12:
		last_day = first_day.replace(year=first_day.year + 1, month=1)
	else:
		last_day = first_day.replace(month=first_day.month + 1)
	
	first_weekday = first_day - datetime.timedelta(first_day.weekday())
	last_weekday = last_day + datetime.timedelta(7 - last_day.weekday())
	
	next_month = last_day + datetime.timedelta(1)
	if int(next_month.year) >= 9999:
		next_month = None
	
	prev_month = first_day - datetime.timedelta(1)
	if int(prev_month.year) <= 1000:
		prev_month = None
	
	month_cal = []
	week = []
	week_headers = []
	
	i = 0
	day = first_weekday
	while day <= last_weekday:
		if i < 7:
			week_headers.append(day)
		cal_day = {}
		cal_day['day'] = day
		cal_day['events'] = event_list.filter(start_date=day).order_by('start_time')
		if day.month == month.month:
			cal_day['in_month'] = True
		else:
			cal_day['in_month'] = False
		if day == datetime.date.today():
			cal_day['today'] = True
		else:
			cal_day['today'] = False
		if day.weekday() == 6 or day.weekday() == 5:
			cal_day['weekend'] = True
		else:
			cal_day['weekend'] = False
		week.append(cal_day)
		if day.weekday() == 6:
			month_cal.append(week)
			week = []
		i += 1
		day += datetime.timedelta(1)
	
	years = range(1986, (datetime.date.today().year + 4))
	
	payload = {
		'calendar': month_cal,
		'headers': week_headers,
		'month': month,
		'next_month': next_month,
		'prev_month': prev_month,
		'today': today,
		'years': years,
		'is_archive': True,
	}
	
	return render_to_response('events/month.html', payload, context_instance=RequestContext(request))

def events_week(request, year=None, week=None):
	if not year:
		year = str(datetime.date.today().year)
	
	if not week:
		week = str(datetime.date.today().isocalendar()[1])
	
	try:
		date = datetime.date(*time.strptime(year + '-0-' + week, '%Y-%w-%U')[:3])
	except ValueError:
		raise Http404
	
	weekdays = [
		{'name': 'Sunday', 'number': 0},
		{'name': 'Monday', 'number': 1},
		{'name': 'Tuseday', 'number': 2},
		{'name': 'Wednsday', 'number': 3},
		{'name': 'Thursday', 'number': 4},
		{'name': 'Friday', 'number': 5},
		{'name': 'Saturday', 'number': 6},
	]
	
	hours = []
	start_time = datetime.datetime.combine(date, datetime.time(0, 0))
	end_time = datetime.datetime.combine(date, datetime.time(23, 0))
	now = start_time
	while now <= end_time:
		hours += [now,]
		now += datetime.timedelta(hours=1)
	
	weekday_count = 0
	for weekday in weekdays:
		weekday['day'] = date + datetime.timedelta(days=weekday_count)
		weekday_count += 1
		morning = datetime.datetime.combine(weekday['day'], datetime.time(0, 0))
		evening = datetime.datetime.combine(weekday['day'], datetime.time(23, 0))
		# TODO I don't like running so many queries.
		events = Event.objects.filter(start_date=weekday['day'])
		all_day = events.filter(start_time__isnull=True)
		
		weekday['agenda'] = []
		now = morning
		while now <= evening:
			end = now + datetime.timedelta(minutes=59)
			agenda_hour = {}
			agenda_hour['start'] = now
			agenda_hour['end'] = end
			agenda_hour['events'] = events.filter(start_time__range=(now.time(), end.time())).order_by('start_time')
			if now.time().hour == datetime.datetime.now().time().hour <= 17:
				agenda_hour['working_hours'] = True
			else:
				agenda_hour['working_hours'] = False
			
			weekday['agenda'] += [agenda_hour,]
			
			now += datetime.timedelta(hours=1)
	
	context_payload = {
		'weekdays': weekdays,
		'date': date,
		'is_archive': True,
		'hours': hours,
	}
	
	return render_to_response('events/week.html', context_payload, context_instance=RequestContext(request))

def events_year(request, year=None):
	if not year:
		year = str(datetime.date.today().year)
	
	prev_year = int(year) - 1
	next_year = int(year) + 1
	
	events = Event.objects.filter(start_date__year=year).dates('start_date', 'month')
	
	months = {}
	
	for i in events:
		month = i.month
		try:
			months[month-1][1] = True
		except KeyError:
			months = [[ datetime.date(int(year), m, 1), False] for m in xrange(1, 13)]
			months[month-1][1] = True
	
	context_payload = {
		'months': months,
		'year': year,
		'next_year': next_year,
		'prev_year': prev_year
	}
	
	return render_to_response('events/year.html', context_payload, context_instance=RequestContext(request))

def events_archives(request):
	events = Event.objects.dates('start_date', 'month')
	
	years = {}
	
	for i in events:
		month = i.month
		year = i.year
		
		try:
			years[year][month-1][1] = True
		except KeyError:
			years[year] = [[ datetime.date(year, m, 1), False ] for m in xrange(1, 13) ]
			years[year][month-1][1] = True
	
	return render_to_response('events/archives.html', { 'years': years }, context_instance=RequestContext(request))

def events_day(request, year=None, month=None, day=None):
	if not year:
		year = str(datetime.date.today().year)
	
	if not month:
		month = datetime.date.today().strftime('%b').lower()
	
	if not day:
		day = str(datetime.date.today().day)
	
	try:
		date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
	except ValueError:
		raise Http404
	
	next_day = date + datetime.timedelta(days=+1)
	prev_day = date + datetime.timedelta(days=-1)
	
	events = Event.objects.filter(start_date=date)
	all_day = events.filter(start_time__isnull=True)
	
	morning = datetime.datetime.combine(date, datetime.time(0, 0))
	evening = datetime.datetime.combine(date, datetime.time(23, 0))
	
	agenda = []
	
	now = morning
	while now <= evening:
		end = now + datetime.timedelta(minutes=59)
		agenda_hour = {}
		agenda_hour['start'] = now
		agenda_hour['end'] = end
		agenda_hour['events'] = events.filter(start_time__range=(now.time(), end.time())).order_by('start_time')
		if now.time().hour == datetime.datetime.now().time().hour:
			agenda_hour['now'] = True
		else:
			agenda_hour['now'] = False
		
		if now.time().hour >= 9 and now.time().hour <= 17:
			agenda_hour['working_hours'] = True
		else:
			agenda_hour['working_hours'] = False
		
		agenda += [agenda_hour,]
		
		now += datetime.timedelta(hours=1)
	
	context_payload = {
		'events': events,
		'agenda': agenda,
		'next_day': next_day,
		'prev_day': prev_day,
		'date': date,
		'all_day': all_day,
		'is_archive': True,
	}
	
	return render_to_response('events/day.html', context_payload, context_instance=RequestContext(request))

def detail(request, year, month, day, slug):
	try:
		date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
	except ValueError:
		raise Http404
	
	try:
		event = Event.objects.get(start_date=date, slug__iexact=slug)
	except IndexError:
		raise Http404
	
	return render_to_response('events/detail.html', { 'event': event, 'date': date }, context_instance=RequestContext(request))

def detail_ical(request, year, month, day, slug):
	try:
		date = datetime.date(*time.strptime(year+month+day, '%Y%b%d')[:3])
	except ValueError:
		raise Http404
	
	try:
		event = Event.objects.get(start_date=date, slug__iexact=slug)
	except IndexError:
		raise Http404
	
	icalendar = export_ical([event, ])
	
	response = HttpResponse(icalendar.as_string(), mimetype="text/calendar")
	response['Content-Disposition'] = 'attachment: filename=%s-%s.ics' % (event.start_date.isoformat(), event.slug)
	
	return response

def ical(request):
	TODAY = datetime.date.today()
	THRIDY_DAYS = datetime.timedelta(days=30)
	
	FUTURE = TODAY + THRIDY_DAYS
	PAST = TODAY - THRIDY_DAYS
	
	event_list = Event.objects.filter(start_date__lte=FUTURE, start_date__gte=PAST)
	
	icalendar = export_ical(event_list)
	
	response = HttpResponse(icalendar.as_string(), mimetype="text/calendar")
	response['Content-Disposition'] = 'attachment: filename=%s-%s.ics' % (FUTURE.isoformat(), PAST.isoformat())
	
	return response

def tag_list(request):
	tags = Event.tags.all()
	
	context = {
		'tags': tags,
		'is_archive': True
	}
	
	return render_to_response('events/tag_list.html', context, context_instance=RequestContext(request))

def tag_detail(request, slug, page=1):
	tag = Event.tags.get(slug=slug)
	event_list = Event.objects.filter(tags__in=[tag])
	
	paginator = Paginator(event_list, 10)
	
	try:
		events = paginator.page(page)
	except (EmptyPage, InvalidPage):
		events = paginator.page(paginator.num_pages)
	
	context = {
		'tag': tag,
		'events': events,
		'is_archive': True
	}
	
	return render_to_response('events/tag_detail.html', context, context_instance=RequestContext(request))

def tag_detail_ical(request, slug):
	tag = Event.tags.get(slug=slug)
	event_list = Event.objects.upcoming(tags__in=[tag])[:10]
	
	icalendar = export_ical(event_list)
	
	response = HttpResponse(icalendar.as_string(), mimetype="text/calendar")
	response['Content-Disposition'] = 'attachment: filename=%s.ics' % slug
	
	return response