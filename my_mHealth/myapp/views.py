from django.http import HttpResponse
from models import ProximityReading
from models import BeaconReading
from models import DeviceUser
import json
from django.shortcuts import render_to_response

ESTIMOTES = {"b9407f30-f5f8-466e-aff9-25556b57fe6d":"Icy Marshmallow"}

# Create your views here.
def index(request):
    return render_to_response('index.html')

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

def beaconUpdate(request):
    beaconOutput = json.loads(request.GET['reading'])
    status = beaconOutput.get("status")
    device_id = beaconOutput.get("device_id")
    estimote_id = beaconOutput.get("prox_uuid")
    deviceOwner = DeviceUser.objects.get(device=device_id)
    new_reading = BeaconReading.objects.create(user=deviceOwner, status=status,beacon=ESTIMOTES.get(estimote_id))
    new_reading.save()
    topReading = BeaconReading.objects.all().order_by("-id")[0]
    return HttpResponse(topReading)

def checkLastBeacon(request):
    topReading = BeaconReading.objects.all().order_by("-id")[0]
    newDict = dict()
    newDict['email'] = topReading.user.email
    newDict['status'] = topReading.status
    newDict['beacon'] = topReading.beacon
    newDict['time'] = topReading.time
    return render_to_response('lastbeacon.html', newDict)

def addUser(request):
    input_user = json.loads(request.GET['newUser'])
    new_email = input_user.get("email")
    new_device = input_user.get("device_id")
    new_user = DeviceUser.objects.get_or_create(email=new_email, device=new_device)
    new_user.save()
    return HttpResponse(new_email)
