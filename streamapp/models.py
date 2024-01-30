from django.db import models


# Create your models here.
class ENV(models.Model):
    name = models.CharField(max_length=10, default=None, null=True)
    TrafficLightState = models.CharField(max_length=10, default=None, null=True)
    timer = models.IntegerField(default=None, null=True)
    interface = models.CharField(max_length=20, default=None, null=True)
    zoneName = models.CharField(max_length=20, default=None, null=True)
    zoneDetectionCoord = models.CharField(max_length=20, default=None, null=True)
    camera = models.CharField(max_length=50, default=None, null=True)
    videoCamera = models.CharField(max_length=50, default=None, null=True)
    isConfigure = models.BooleanField(default=False)
    nbOfCars = models.IntegerField(default=None, null=True)

    def __str__(self):
        return self.name

    def getIsConfigure(self):
        return self.isConfigure

    def getCamera(self):
        return self.camera

    def getId(self):
        return self.pk

    def getName(self):
        return self.name

    def getZoneName(self):
        return self.zoneName

    def getZoneDetectionCoord(self):
        return self.zoneDetectionCoord

    def getVideoCamera(self):
        return self.videoCamera
