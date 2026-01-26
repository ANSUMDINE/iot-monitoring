from rest_framework import serializers
from .models import Sensor, Measurement

class SensorSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sensor
        fields = ['id', 'name', 'location', 'sensor_type']


class MeasurementSerializer(serializers.ModelSerializer):
    sensor = SensorSerializer(read_only=True)
    sensor_id = serializers.PrimaryKeyRelatedField(
        queryset=Sensor.objects.all(), source='sensor', write_only=True
    )

    class Meta:
        model = Measurement
        fields = ['id', 'sensor', 'sensor_id', 'value', 'unit', 'created_at']

    def validate_value(self, value):
        if value < -50 or value > 100:
            raise serializers.ValidationError("Valeur hors plage : -50 à +100 °C attendue.")
        return value

    def validate_unit(self, unit):
        allowed_units = ['°C', '%', 'lux']
        if unit not in allowed_units:
            raise serializers.ValidationError(f"Unité invalide. Choisir parmi : {allowed_units}")
        return unit
