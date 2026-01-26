import logging
from rest_framework import generics, permissions
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response

logger = logging.getLogger(__name__)


class SensorListCreateView(generics.ListCreateAPIView):
    queryset = Sensor.objects.all()
    serializer_class = SensorSerializer
    permission_classes = [permissions.IsAuthenticated]


class MeasurementListCreateView(generics.ListCreateAPIView):
    queryset = Measurement.objects.all().order_by('-created_at')
    serializer_class = MeasurementSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        try:
            serializer.save()
        except Exception as e:
            logger.error(f"Erreur lors de l'enregistrement : {e}")
            raise

    def get_queryset(self):
        queryset = super().get_queryset()
        sensor_id = self.request.query_params.get('sensor_id')
        start = self.request.query_params.get('start')
        end = self.request.query_params.get('end')

        if sensor_id:
            queryset = queryset.filter(sensor_id=sensor_id)
        if start:
            queryset = queryset.filter(created_at__gte=start)
        if end:
            queryset = queryset.filter(created_at__lte=end)

        return queryset


class LastMeasurementView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def get(self, request, sensor_id):
        try:
            measurement = Measurement.objects.filter(sensor_id=sensor_id).latest('created_at')
        except Measurement.DoesNotExist:
            return Response({"detail": "No measurement found"}, status=404)

        serializer = MeasurementSerializer(measurement)
        return Response(serializer.data)
