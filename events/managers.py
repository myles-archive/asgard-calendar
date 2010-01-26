from datetime import datetime
import operator

from django.db.models import Manager, Q

class EventManager(Manager):
	"""
	Same as above but for templates
	"""
	
	def public(self, **kwargs):
		return self.get_query_set().filter(private=True, **kwargs)
	
	def published(self, **kwargs):
		return self.get_query_set().filter(published__lte=datetime.now(), private=True, **kwargs)
	
	def search(self, search_terms):
		terms = [term.strip() for term in search_terms.split()]
		q_objects = []
		
		for term in terms:
			q_objects.append(Q(title__icontains=term))
			q_objects.append(Q(body_html__icontains=term))
		
		qs = self.get_query_set().filter(published__lte=datetime.now())
		return qs.filter(reduce(operator.or_, q_objects))
