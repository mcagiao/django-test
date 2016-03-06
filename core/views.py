from django.shortcuts import render, HttpResponse
from django.http import JsonResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Raspberry, Data

import json

class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

def info(request):
    return JsonResponse({'server': 'Gpul server'})

@csrf_exempt
def postData(request):
    jsonData = json.loads(request.body.decode())
    device = jsonData['device']
    mac = device['mac']
    hostname = device['hostname']
    ip = request.META.get('REMOTE_ADDR')
    try:
        raspberry = Raspberry.objects.get(mac=mac)
    except:
        print('New mac detected, creating raspberry')
        raspberry = Raspberry(mac=mac, ip=ip, hostname=hostname)
        raspberry.save()

    data = jsonData['data']
    name = data['name'].upper()
    value = data['value']
    d = Data(name=name, value=value, device=raspberry)
    d.save()

    return JsonResponse({'result': 'Ok'})

class RaspberryListView(generic.ListView):
    model = Raspberry
    template_name = 'core/raspberry-list.html'

class RaspberryDetailView(generic.DetailView):
    model = Raspberry
    template_name = 'core/raspberry-detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['data_list'] = Data.objects.filter(device=self.object)
        return context

def raspberryData(request, pk, name):
    d = Data.objects.filter(device=pk, name=name.upper()).last()
    return JsonResponse({'value': d.value})
