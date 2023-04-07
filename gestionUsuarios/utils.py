# calendarapp/utils.py

from datetime import datetime, timedelta
from calendar import HTMLCalendar
from .models import Event
import math, random 
#from eventcalendar.helper import get_current_user

class Calendar(HTMLCalendar):
	def __init__(self, year=None, month=None):
		self.year = year
		self.month = month
		super(Calendar, self).__init__()

	# formats a day as a td
	# filter events by day
	def formatday(self, day, events):
		events_per_day = events.filter(Tiempo_inicial__day=day)
		d = ''
		
		for event in events_per_day:
			d += f'<li> {event.get_html_url} </li>'
		
		if day != 0:
			return f"<td><span class='date'>{day}</span><ul> {d} </ul></td>"
		return '<td></td>'

	# formats a week as a tr 
	def formatweek(self, theweek, events):
		week = ''
		for d, weekday in theweek:
			week += self.formatday(d, events)
		return f'<tr> {week} </tr>'

	# formats a month as a table
	# filter events by year and month
	def formatmonth(self, withyear=True):
		events = Event.objects.filter(Tiempo_inicial__year=self.year, Tiempo_inicial__month=self.month)

		cal = f'<table border="0" cellpadding="0" cellspacing="0" class="calendar">\n'
		cal += f'{self.formatmonthname(self.year, self.month, withyear=withyear)}\n'
		cal += f'{self.formatweekheader()}\n'
		for week in self.monthdays2calendar(self.year, self.month):
			cal += f'{self.formatweek(week, events)}\n'
		return cal
	

def generate_class_code(total_digits,existing_codes) :  
    digits = ''.join([str(i) for i in range(0,10)])
    code = ""  
    while True:
        for i in range(total_digits) : 
            code += digits[math.floor(random.random() * 10)] 
        if code not in existing_codes:
            print('Code not in existing codes')
            break
    return code 