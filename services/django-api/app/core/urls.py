from django.urls import path

from .views import (
    device_detail,
    device_list_create,
    gateway_detail,
    gateway_list_create,
    health,
    index,
    overview,
    system_ports,
    telemetry_detail,
    telemetry_list_create,
    video_status,
)

urlpatterns = [
    path('', index, name='index'),
    path('health/', health, name='health'),
    path('overview/', overview, name='overview'),
    path('video/status/', video_status, name='video-status'),
    path('system/ports/', system_ports, name='system-ports'),
    path('gateways/', gateway_list_create, name='gateway-list-create'),
    path('gateways/<int:pk>/', gateway_detail, name='gateway-detail'),
    path('devices/', device_list_create, name='device-list-create'),
    path('devices/<int:pk>/', device_detail, name='device-detail'),
    path('telemetry/', telemetry_list_create, name='telemetry-list-create'),
    path('telemetry/<int:pk>/', telemetry_detail, name='telemetry-detail'),
]
