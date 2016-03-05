from django.shortcuts import render, HttpResponse
from django.views import generic
from django.views.decorators.csrf import csrf_exempt

import json

class IndexView(generic.TemplateView):
    template_name = 'core/index.html'

@csrf_exempt
def postData(request):
    data = json.dumps('ok')
    data = json.dumps(request.POST)
    return HttpResponse(data, content_type='application/json')
