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

from datetime import datetime
import operator

from django.db.models import Manager, Q

class EventManager(Manager):
	"""
	Same as above but for templates
	"""
	
	def published(self, **kwargs):
		return self.get_query_set().filter(published__lte=datetime.now(), **kwargs)
	
	def search(self, search_terms):
		terms = [term.strip() for term in search_terms.split()]
		q_objects = []
	
		for term in terms:
			q_objects.append(Q(title__icontains=term))
			q_objects.append(Q(body_html__icontains=term))
	
		qs = self.get_query_set().filter(published__lte=datetime.now())
		return qs.filter(reduce(operator.or_, q_objects))
