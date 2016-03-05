from django.shortcuts import render, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

from .models import Raspberry, Data

import json

class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

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

    data = json.dumps('ok')
    return HttpResponse(data, content_type='application/json')
