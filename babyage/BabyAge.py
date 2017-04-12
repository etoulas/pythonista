import ui
import datetime
from dateutil import rrule

	
def between_dates(rule, start_date, end_date):
	weeks = rrule.rrule(rule, dtstart=start_date, until=end_date)
	return weeks.count()

DOB = datetime.datetime.now()
NOW = datetime.datetime.now()

full_weeks = (NOW - DOB).days/7

weeks = between_dates(rrule.WEEKLY, DOB, NOW)
months = between_dates(rrule.MONTHLY, DOB, NOW)
years = between_dates(rrule.YEARLY, DOB, NOW)

#print 'Full weeks {}'.format(full_weeks)
#print '{}th week'.format(weeks)
#print 'Months {}'.format(months)


def datepicker_action(sender):
	dob = sender.date
	weeks = between_dates(rrule.WEEKLY, dob, NOW)
	months = between_dates(rrule.MONTHLY, dob, NOW)
	years = between_dates(rrule.YEARLY, dob, NOW)
	
	v = sender.superview
	v['weeks'].text = str(weeks) + '.'
	v['months'].text = str(months) + '.'
	v['years'].text = str(years) + '.'


v = ui.load_view('BabyAge')

v['datepicker'].date = DOB
v['weeks'].enabled = False
v['months'].enabled = False
v['years'].enabled = False
v['weeks'].text = str(weeks) + '.'
v['months'].text = str(months) + '.'
v['years'].text = str(years) + '.'

v.present('sheet')



