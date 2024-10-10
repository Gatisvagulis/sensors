from django.urls import path
from .views import SensorDataView, MetricsDataView, SensorTypesDataView

urlpatterns = [
    path('sensors/', SensorDataView.as_view(), name='sensor-data'),
    path('metrics/', MetricsDataView.as_view(), name='metric-data'),
    path('sensors-type/', SensorTypesDataView.as_view(), name='sensor-type'),
]
