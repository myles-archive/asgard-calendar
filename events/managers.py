from datetime import datetime
import operator

from django.db.models import Manager, Q

class EventManager(Manager):
	"""
	Same as above but for templates
	"""
	
	def upcoming(self, **kwargs):
		"""
		Upcoming events.
		"""
		TODAY = datetime.now()
		return self.get_query_set().filter(private=False,
			start_date__gte=TODAY.date(), **kwargs).order_by('start_date')
	
	def public(self, **kwargs):
		"""
		Public events.
		"""
		return self.get_query_set().filter(private=False, **kwargs)
	
	def published(self, **kwargs):
		"""
		Published events.
		"""
		return self.get_query_set().filter(private=False,
			published__lte=datetime.now(), **kwargs)
	
	def search(self, search_terms):
		"""
		A simple ORM based search.
		"""
		terms = [term.strip() for term in search_terms.split()]
		q_objects = []
		
		for term in terms:
			q_objects.append(Q(title__icontains=term))
			q_objects.append(Q(body_html__icontains=term))
		
		qs = self.get_query_set().filter(
			published__lte=datetime.now())
		
		return qs.filter(reduce(operator.or_, q_objects))
