import json
from django.http import JsonResponse
from django.views import View

class SensorDataView(View):
    def get(self, request, *args, **kwargs):
        with open('polls/sensors.json', 'r') as file:
            sensor_data = json.load(file)
        return JsonResponse(sensor_data, safe=False)

class MetricsDataView(View):
    def get(self, request, *args, **kwargs):
        with open('polls/metrics.json', 'r') as file:
            metrics_data = json.load(file)
        return JsonResponse(metrics_data, safe=False)

class SensorTypesDataView(View):
    def get(self, request, *args, **kwargs):
        with open('polls/sensorTypes.json', 'r') as file:
            sensor_types_data = json.load(file)
        return JsonResponse(sensor_types_data, safe=False)
