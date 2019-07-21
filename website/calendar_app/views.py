from django.shortcuts import render, redirect
from datetime import datetime, timedelta, date
from django.shortcuts import render, get_object_or_404
from django.http import HttpResponse, HttpResponseRedirect
from django.views import generic
from django.urls import reverse
from datetime import datetime
from django.utils.safestring import mark_safe
import calendar
from .forms import *
from .models import *
from .utils import Calendar
import requests
from django.utils import timezone
import json
from datetime import date
import calendar


def convert24(str1):

    if str1[-2:] == "AM" and str1[:2] == "12":
        return "00" + str1[2:-2]

    # remove the AM
    elif str1[-2:] == "AM":
        return str1[:-2]

    elif str1[-2:] == "PM" and str1[:2] == "12":
        return str1[:-2]

    else:

        return str(int(str1[:2]) + 12) + str1[2:8]



def time_difference(time_start, time_end):

    start = datetime.strptime(time_start, "%H%M")
    end = datetime.strptime(time_end, "%H%M")
    difference = end - start
    minutes = difference.total_seconds() / 60
    return int(minutes)

def add_time(time_start, minutes):

    start = datetime.strptime(time_start, "%H%M")
    end = start + timedelta(minutes=minutes)
    return end

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
            city = key.get('Enter_your_location')
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

                date_details = data['feedCreation']
                year = int(date_details[0:4])
                month = int(date_details[5:7])
                date_num = int(date_details[8:10])
                week_day = date(year, month, date_num).weekday()
                if week_day==0 :
                    gulika = 6
                    raahu = 2
                    yama = 4
                elif week_day==1 :
                    gulika = 5
                    raahu = 7
                    yama = 3
                elif week_day==2 :
                    gulika = 4
                    raahu = 5
                    yama = 2
                elif week_day==3 :
                    gulika = 3
                    raahu = 6
                    yama = 1
                elif week_day==4 :
                    gulika = 2
                    raahu = 4
                    yama = 8
                elif week_day==5 :
                    gulika = 1
                    raahu = 3
                    yama = 7
                else :
                    gulika = 7
                    raahu = 8
                    yama = 5

                sunrise = data['astronomy']['astronomy'][0]['sunrise'][0:4]
                sunset = data['astronomy']['astronomy'][0]['sunset'][0:4]
                sunrise = "0"+sunrise+":00 "+data['astronomy']['astronomy'][0]['sunrise'][4:6]
                sunset = "0"+sunset+":00 "+data['astronomy']['astronomy'][0]['sunset'][4:6]
                sunrise = convert24(sunrise)
                sunset = convert24(sunset)
                sunrise = sunrise[0:2]+sunrise[3:5]
                sunset = sunset[0:2] + sunset[3:5]

                time_diff = time_difference(sunrise,sunset)
                time_unit_diff = time_diff/8

                raahu_kaala_start = add_time(sunrise,(raahu-1)*time_unit_diff).time()
                raahu_kaala_end = add_time(sunrise,(raahu)*time_unit_diff).time()

                yama_kaala_start = add_time(sunrise, (yama - 1) * time_unit_diff).time()
                yama_kaala_end = add_time(sunrise, (yama) * time_unit_diff).time()

                gulika_kaala_start = add_time(sunrise, (gulika - 1) * time_unit_diff).time()
                gulika_kaala_end = add_time(sunrise, (gulika) * time_unit_diff).time()

                yama_kaala_start = yama_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                yama_kaala_end = yama_kaala_end.strftime("%H:%M:%S.%f")[0:8]
                gulika_kaala_start = gulika_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                gulika_kaala_end = gulika_kaala_end.strftime("%H:%M:%S.%f")[0:8]
                raahu_kaala_start = raahu_kaala_start.strftime("%H:%M:%S.%f")[0:8]
                raahu_kaala_end = raahu_kaala_end.strftime("%H:%M:%S.%f")[0:8]

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
                    'date': data['feedCreation'][0:10],
                    'raahu_kaala_s': raahu_kaala_start,
                    'raahu_kaala_e': raahu_kaala_end,
                    'gulika_kaala_s': gulika_kaala_start,
                    'gulika_kaala_e': gulika_kaala_end,
                    'yama_kaala_s': yama_kaala_start,
                    'yama_kaala_e': yama_kaala_end,
                }))

    return render(request, 'cal/geo.html', {'form': form, })
