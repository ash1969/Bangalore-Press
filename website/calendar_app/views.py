from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from django.utils.safestring import mark_safe
import calendar
from .forms import *
from .models import *
from .utils import Calendar
import requests
from django.utils import timezone
import json

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

def geo(request):
    form = Locationform(request.POST or None)

    if request.method == 'POST':
       if request.POST.get('ajax_check') == "True":
         if form.is_valid():
            key = form.cleaned_data
            city = key.get('location')
            url = 'https://weather.cit.api.here.com/weather/1.0/report.json'

            parameters = dict(
                product='forecast_astronomy',
                name=city,
                app_id='cTqOSjbtmgQB1XGtr5SB',
                app_code='9tCOayrEASzoc6cLYeK_wQ'
            )

            response = requests.get(url=url, params=parameters)
            data = response.json()

            x = "Type" in data
            if x == True:
                return HttpResponse("No City Found")
            else:
                print(data)

                # Calculations
                #
                #
                #
                #
                # Calculations

                return HttpResponse(json.dumps({
                    'sunrise': data['astronomy']['astronomy'][0]['sunrise'],
                    'sunset': data['astronomy']['astronomy'][0]['sunset'],
                    'moonrise': data['astronomy']['astronomy'][0]['moonrise'],
                    'moonset': data['astronomy']['astronomy'][0]['moonset'],
                    'country': data['astronomy']['country'],
                    'state': data['astronomy']['state'],
                    'timezone': data['astronomy']['timezone'],
                    'latitude': data['astronomy']['latitude'],
                    'longitude': data['astronomy']['longitude'],
                }))

    return render(request, 'cal/geo.html', {'form': form, })
