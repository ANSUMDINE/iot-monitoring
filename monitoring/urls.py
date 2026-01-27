from django.urls import path
from .views import SensorListCreateView, MeasurementListCreateView, LastMeasurementView, SensorIdListView
from .views import UserLinkedSensorsLastView
from .views import UserSensorCreateView
from .views import SensorMeasurementsView
from .views import UserSensorListView
from .views import UserSensorDeleteView




urlpatterns = [
    path('sensors/', SensorListCreateView.as_view(), name='sensor-list-create'),
    path('measurements/', MeasurementListCreateView.as_view(), name='measurement-list-create'),
    path('measurements/last/<int:sensor_id>/', LastMeasurementView.as_view(), name='last-measurement'),
]


urlpatterns += [
    path('sensors/ids/', SensorIdListView.as_view(), name='sensor-id-list'),
    path('users/<int:user_id>/sensors/latest/', UserLinkedSensorsLastView.as_view(), name='user-sensors-latest'),
    path('user-sensors/', UserSensorCreateView.as_view(), name='user-sensor-create'),
    path('sensors/<int:sensor_id>/measurements/', SensorMeasurementsView.as_view(), name='sensor-measurements'),
    path('user-sensors/list/', UserSensorListView.as_view(), name='user-sensor-list'),
    path('user-sensors/delete/', UserSensorDeleteView.as_view(), name='user-sensor-delete'),
]
