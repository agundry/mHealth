from django.db import models

# Create your models here.
class ProximityReading(models.Model):
    id = models.AutoField(primary_key=True)
    value = models.IntegerField(default=0)
    message = models.CharField(max_length=30, blank=False)

class DeviceUser(models.Model):
    id = models.AutoField(primary_key=True)
    email = models.EmailField(max_length=40, default='')
    device = models.CharField(max_length=50, blank=False, default='')

    def __repr__(self):
        return 'DeviceUser(id={}, email={}, device={})'.format(self.id, self.email, self.device)

class BeaconReading(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(DeviceUser)
    status = models.CharField(max_length=10, blank=False, default='')
    beacon = models.CharField(max_length=40, blank=False, default='')
    major = models.CharField(max_length=6, blank=False, default='')
    minor = models.CharField(max_length=6, blank=False, default='')
    time = models.DateTimeField(auto_now_add=True)

    def __repr__(self):
        return 'BeaconReading(id={}, user={}, status={}, beacon={}, major={}, minor={}, time={}'.format(self.id, self.user, self.status, self.beacon, self.major, self.minor, self.time)
