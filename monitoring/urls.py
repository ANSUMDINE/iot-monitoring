from django.urls import path
from .views import SensorListCreateView, MeasurementListCreateView, LastMeasurementView


urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('measurements/', MeasurementListCreateView.as_view(), name='measurement-list-create'),
    path('measurements/last/<int:sensor_id>/', LastMeasurementView.as_view(), name='last-measurement'),
]
