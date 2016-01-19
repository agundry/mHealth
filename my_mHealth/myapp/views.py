from django.http import HttpResponse
from models import ProximityReading
import json
from django.shortcuts import render_to_response

# Create your views here.
def index(request):
    return render_to_response('hello.html')

# Records new value from sensor
def sensor(request):
    sensorValue = json.loads(request.GET['value'])[u'value']
    newMessage = "Hello" if sensorValue == 0 else "World"
    new_observation = ProximityReading.objects.create(value=0.0, message=newMessage)
    new_observation.save()
    topObservation = ProximityReading.objects.all().order_by("-id")[0]
    return HttpResponse(topObservation.message)

# Fetches the newest value of sensor from database
def update(request):
    topObservation = ProximityReading.objects.all().order_by("-id")[0]
    return HttpResponse(topObservation.message)

