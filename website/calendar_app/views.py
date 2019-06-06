from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar

from .models import *
from .utils import Calendar

from django.utils import timezone

def home(request):
    args={}
    return render(request, 'cal/home.html', args)

def authentication(request):
    if request.user.is_authenticated:
        return redirect('cal:calendar')
    args={}
    return render(request, 'cal/authenticate.html', args)

class CalendarView(generic.ListView):
    model = Festivals
    template_name = 'cal/calendar.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        d = get_date(self.request.GET.get('month', None))
        cal = Calendar(d.year, d.month)
        html_cal = cal.formatmonth(withyear=True)
        context['calendar'] = mark_safe(html_cal)
        context['prev_month'] = prev_month(d)
        context['next_month'] = next_month(d)
        start_date = timezone.now()
        end_date = start_date + timedelta(days=30) #Using this to display festivals with dates within next 30 days
        context['festivals_display'] = Festivals.objects.filter(date__range=[start_date, end_date]).order_by('date') #Collecting the most recent upcoming events to display below the calendar
        return context

def get_date(req_month):
    if req_month:
        year, month = (int(x) for x in req_month.split('-'))
        return date(year, month, day=1)
    return datetime.today()

def prev_month(d):
    first = d.replace(day=1)
    prev_month = first - timedelta(days=1)
    month = 'month=' + str(prev_month.year) + '-' + str(prev_month.month)
    return month

def next_month(d):
    days_in_month = calendar.monthrange(d.year, d.month)[1]
    last = d.replace(day=days_in_month)
    next_month = last + timedelta(days=1)
    month = 'month=' + str(next_month.year) + '-' + str(next_month.month)
    return month

def festival_detail(request, event_id=None):
    try:
        instance = get_object_or_404(Festivals, pk=event_id)
    except:
        return HttpResponse("Id Does Not Exist!")
    return render(request, 'cal/festival.html', {'festival': instance})
