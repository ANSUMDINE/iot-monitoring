import logging
from rest_framework import generics, permissions
from .models import Sensor, Measurement
from .serializers import SensorSerializer, MeasurementSerializer
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import Sensor
from django.contrib.auth.models import User
from .models import UserSensor

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

class SensorIdListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        ids = Sensor.objects.values_list('id', flat=True).distinct()
        return Response({"sensor_ids": list(ids)})




class UserLinkedSensorsLastView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, user_id):
        try:
            user = User.objects.get(id=user_id)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable"}, status=404)

        # Si admin → voir tous les capteurs
        if hasattr(user, "profile") and user.profile.is_admin:
            sensor_ids = Sensor.objects.values_list('id', flat=True)
        else:
            sensor_ids = UserSensor.objects.filter(user=user).values_list('sensor_id', flat=True)

        data = []
        for sensor_id in sensor_ids:
            try:
                last_measure = Measurement.objects.filter(sensor_id=sensor_id).latest('created_at')
                data.append({
                    "sensor_id": sensor_id,
                    "value": last_measure.value,
                    "unit": last_measure.unit,
                    "timestamp": last_measure.created_at
                })
            except Measurement.DoesNotExist:
                continue

        return Response(data)

class UserSensorCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        user_id = request.data.get("user_id")
        sensor_id = request.data.get("sensor_id")

        if not user_id or not sensor_id:
            return Response({"detail": "user_id et sensor_id sont requis"}, status=400)

        try:
            user = User.objects.get(id=user_id)
            sensor = Sensor.objects.get(id=sensor_id)
        except User.DoesNotExist:
            return Response({"detail": "Utilisateur introuvable"}, status=404)
        except Sensor.DoesNotExist:
            return Response({"detail": "Capteur introuvable"}, status=404)

        # Empêcher les doublons
        link, created = UserSensor.objects.get_or_create(user=user, sensor=sensor)

        if not created:
            return Response({"detail": "Lien déjà existant"}, status=200)

        return Response({"detail": "Lien créé avec succès"}, status=201)
    
class SensorMeasurementsView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, sensor_id):
        measurements = Measurement.objects.filter(sensor_id=sensor_id).order_by('-created_at')
        serializer = MeasurementSerializer(measurements, many=True)
        return Response(serializer.data)
    
class UserSensorListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        links = UserSensor.objects.all().select_related("user", "sensor")
        data = []

        for link in links:
            data.append({
                "id": link.id,
                "user": {
                    "id": link.user.id,
                    "username": link.user.username
                },
                "sensor": {
                    "id": link.sensor.id,
                    "name": link.sensor.name,
                    "location": link.sensor.location,
                    "sensor_type": link.sensor.sensor_type
                }
            })

        return Response(data)

class UserSensorDeleteView(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request):
        user_id = request.data.get("user_id")
        sensor_id = request.data.get("sensor_id")

        if not user_id or not sensor_id:
            return Response({"detail": "user_id et sensor_id sont requis"}, status=400)

        try:
            link = UserSensor.objects.get(user_id=user_id, sensor_id=sensor_id)
        except UserSensor.DoesNotExist:
            return Response({"detail": "Lien introuvable"}, status=404)

        link.delete()
        return Response({"detail": "Lien supprimé avec succès"}, status=200)

