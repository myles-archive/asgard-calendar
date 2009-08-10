import datetime

from django import forms
from django.utils.translation import ugettext_lazy as _

MONTH_CHOICES = (
	('jan', _('January')),
	('feb', _('February')),
	('mar', _('March')),
	('may', _('May')),
	('jun', _('June')),
	('jul', _('July')),
	('aug', _('August')),
	('sep', _('September')),
	('oct', _('October')),
	('nov', _('November')),
	('dec', _('December'))
)

class CalendarYearMonthForm(forms.Form):
	month = forms.ChoiceField(required=False, choices=MONTH_CHOICES)
	year = forms.IntegerField(required=False)