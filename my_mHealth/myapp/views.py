from django.http import HttpResponse
from .models import ProximityReading, BeaconReading, DeviceUser
from datetime import datetime, timedelta
from django.utils import timezone
import json
from django.shortcuts import render_to_response

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
    majorID = beaconOutput.get("major")
    minorID = beaconOutput.get("minor")
    deviceOwner = DeviceUser.objects.get(device=device_id)
    new_reading = BeaconReading.objects.create(user=deviceOwner, status=status,beacon=estimote_id, major=majorID, minor=minorID)
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
    return HttpResponse(new_email)

def deleteReadings(request):
    BeaconReading.objects.all().delete()
    return render_to_response('delete.html')

def checkBeaconSinceTime(request):
    # input_time = json.loads(request.GET['time'])
    readingsSinceTime = BeaconReading.objects.filter(time__gte=timezone.now()-timedelta(days=4))
    return HttpResponse(readingsSinceTime.values())

def infectionReport(request):
    return render_to_response('infectionReport.html')

def searchConnections(request):
    infected_email = request.GET['email']
    infected_user = DeviceUser.objects.get(email=infected_email)
    readings_since_incubation = BeaconReading.objects.filter(time__gte=timezone.now()-timedelta(days=3), user=infected_user)

    # build dictionary keyed on beacons that contains all readings for that beacon
    infection_beacons = build_infection_dict(readings_since_incubation)

    # create dictionary that will have tuples associated with enter/exits of beacons
    infection_tuples = build_infection_tuples(infection_beacons, readings_since_incubation)

    # search for other users
    all_users = DeviceUser.objects.all()
    overlap_dict = dict()
    for _user in all_users:
        if _user != infected_user:
            user_readings = BeaconReading.objects.filter(time__gte=timezone.now()-timedelta(days=3), user=_user)
            _infection_beacons = build_infection_dict(user_readings)
            _infection_tuples = build_infection_tuples(_infection_beacons, user_readings)
            _overlaps = find_overlaps(infection_tuples, _infection_tuples)
            overlap_dict[_user.email] = _overlaps

    # get beacons where overlaps occured
    for key in overlap_dict.keys():
        for i in range(len(overlap_dict[key])):
            interval = overlap_dict[key].pop(0)
            overlap_dict[key].append((interval, BeaconReading.objects.get(time=interval[0]).beacon))


    return HttpResponse(str(overlap_dict))

def build_infection_dict(readings):
    infection_dict = dict()
    for reading in readings:
        if not infection_dict.get(reading.major):
            infection_dict[reading.major] = list()
        infection_dict[reading.major].append(reading)

    return infection_dict

def build_infection_tuples(infection_dict, readings):
    infection_tuples = dict()
    last_reading = None
    for key in infection_dict.keys():
        infection_tuples[key] = list()

    # edge case for exit without enter
    if readings[0].status == 'exit':
        infection_tuples[readings[0].major].append((timezone.now() - timedelta(days=3), readings.pop(0).time))

    # edge case for enter without exit
    if len(readings) % 2 != 0:
        last_reading = readings.pop(len(readings) - 1)

    # format statuses into tuples
    for key in infection_dict.keys():
        for reading in infection_dict[key]:
            infection_tuples[key].append((infection_dict[key].pop(0).time, infection_dict[key].pop(0).time))

    # add in last enter if applicable
    if last_reading:
        infection_tuples[last_reading.major].append((last_reading.time, timezone.now()))

    return infection_tuples

def find_overlaps(infected_tuples, bystander_tuples):
    overlaps = list()
    for key in infected_tuples.keys():
        if bystander_tuples.get(key):
            for i_tuple in infected_tuples[key]:
                for b_tuple in bystander_tuples[key]:
                    if (i_tuple[0] <= b_tuple[0] <= i_tuple[1]) or (b_tuple[0] <= i_tuple[0] <= b_tuple[1]):
                        overlaps.append((max(i_tuple[0],b_tuple[0]), min(i_tuple[1], b_tuple[1])))
    return overlaps

