from django.db import models

class Sensor(models.Model):
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100, blank=True, null=True)
    sensor_type = models.CharField(max_length=50)  

    def __str__(self):
        return f"{self.name} ({self.sensor_type})"


class Measurement(models.Model):
    sensor = models.ForeignKey(Sensor, on_delete=models.CASCADE, related_name='measurements')
    value = models.FloatField()
    unit = models.CharField(max_length=20)  # °C, %, lux, etc.
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.sensor.name} = {self.value} {self.unit} @ {self.created_at}"
