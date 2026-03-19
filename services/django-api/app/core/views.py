from pathlib import Path

import requests
from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .demo_data import PORTS_PAYLOAD
from .models import Device, Gateway, Telemetry
from .serializers import DeviceSerializer, GatewaySerializer, TelemetrySerializer

PROJECT_ROOT = Path('/app')


def _parse_int(value, default=None, minimum=None, maximum=None):
    try:
        parsed = int(value)
    except (TypeError, ValueError):
        return default

    if minimum is not None and parsed < minimum:
        parsed = minimum
    if maximum is not None and parsed > maximum:
        parsed = maximum
    return parsed


def _video_status_payload():
    wvp_jar_path = Path('/app/project-data/wvp/wvp-pro.jar')
    zlm_config_path = Path('/app/docker/zlm/config.ini')
    wvp_config_path = Path('/app/docker/wvp/application-docker.yml')

    zlm_status = 'configured'
    wvp_status = 'placeholder' if not wvp_jar_path.exists() else 'running-candidate'
    wvp_probe = {'reachable': False}
    zlm_probe = {'reachable': False}
    wvp_runtime = {
        'login_ready': False,
        'admin_user_present': False,
        'media_server_count': 0,
        'media_server_online': 0,
        'server_id': None,
        'api_doc_ready': False,
        'frontend_ready': False,
    }

    if wvp_jar_path.exists():
        try:
            response = requests.get('http://edge-wvp:18978/api/server/media_server/list', timeout=3)
            if response.status_code in (200, 401):
                wvp_probe['reachable'] = True
                if response.status_code == 401:
                    wvp_status = 'running'
        except requests.RequestException:
            pass

        try:
            response = requests.post('http://zlm/index/api/getServerConfig', data={'secret': '0'}, timeout=3)
            if response.ok:
                payload = response.json()
                zlm_probe['reachable'] = payload.get('code') == 0
                if zlm_probe['reachable']:
                    zlm_status = 'running'
        except (requests.RequestException, ValueError):
            pass

        try:
            login_response = requests.get(
                'http://edge-wvp:18978/api/user/login',
                params={
                    'username': 'admin',
                    'password': '21232f297a57a5a743894a0e4a801fc3',
                },
                timeout=3,
            )
            if login_response.ok:
                login_payload = login_response.json()
                token = login_payload.get('data', {}).get('accessToken')
                wvp_runtime['login_ready'] = bool(token)
                wvp_runtime['admin_user_present'] = login_payload.get('data', {}).get('username') == 'admin'
                wvp_runtime['server_id'] = login_payload.get('data', {}).get('serverId')
                if token:
                    media_response = requests.get(
                        'http://edge-wvp:18978/api/server/media_server/list',
                        headers={'access-token': token},
                        timeout=3,
                    )
                    if media_response.ok:
                        media_payload = media_response.json().get('data') or []
                        wvp_runtime['media_server_count'] = len(media_payload)
                        wvp_runtime['media_server_online'] = sum(1 for item in media_payload if item.get('status'))
        except (requests.RequestException, ValueError):
            pass

        try:
            api_doc_response = requests.get('http://edge-wvp:18978/v3/api-docs', timeout=3)
            wvp_runtime['api_doc_ready'] = api_doc_response.ok
        except requests.RequestException:
            pass

        try:
            frontend_response = requests.get('http://edge-wvp:18978/', timeout=3)
            wvp_runtime['frontend_ready'] = frontend_response.ok and 'WVP视频平台' in frontend_response.text
        except requests.RequestException:
            pass

    return {
        'enabled': True,
        'zlm': {
            'status': zlm_status,
            'http_url': 'http://localhost:28082',
            'rtmp_port': 19350,
            'rtsp_port': 15540,
            'rtc_port': 11000,
            'config_exists': zlm_config_path.exists(),
            'probe': zlm_probe,
        },
        'wvp': {
            'status': wvp_status,
            'http_url': 'http://localhost:28080',
            'sip_tcp_port': 28116,
            'sip_udp_port': 28116,
            'rtp_udp_range': '13000-13100',
            'config_exists': wvp_config_path.exists(),
            'jar_exists': wvp_jar_path.exists(),
            'jar_path': str(wvp_jar_path),
            'probe': wvp_probe,
            'runtime': wvp_runtime,
        },
    }


def _stats_payload():
    return {
        'gateway_count': Gateway.objects.count(),
        'device_count': Device.objects.count(),
        'telemetry_count': Telemetry.objects.count(),
        'online_gateway_count': Gateway.objects.filter(status='online').count(),
        'online_device_count': Device.objects.filter(status='online').count(),
    }


@api_view(['GET'])
def health(request):
    return Response({
        'status': 'ok',
        'service': 'django-api',
        'timestamp': timezone.now().isoformat(),
    })


@api_view(['GET'])
def overview(request):
    latest_telemetry = Telemetry.objects.select_related('gateway', 'device').order_by('-collected_at', '-created_at')[:10]
    latest_data = TelemetrySerializer(latest_telemetry, many=True).data

    video = _video_status_payload()
    return Response({
        'stats': _stats_payload(),
        'latest_telemetry': latest_data,
        'video': video,
        'video_runtime': {
            'wvp': video.get('wvp', {}).get('runtime', {}),
            'zlm': video.get('zlm', {}).get('probe', {}),
        },
    })


@api_view(['GET'])
def video_status(request):
    return Response(_video_status_payload())


@api_view(['GET'])
def video_runtime(request):
    video = _video_status_payload()
    return Response({
        'status': video.get('wvp', {}).get('status'),
        'wvp': video.get('wvp', {}),
        'zlm': video.get('zlm', {}),
    })


@api_view(['GET'])
def system_ports(request):
    return Response(PORTS_PAYLOAD)


@api_view(['GET'])
def system_status(request):
    latest_telemetry = Telemetry.objects.select_related('gateway', 'device').order_by('-collected_at', '-created_at')[:5]
    video = _video_status_payload()
    return Response({
        'status': 'ok',
        'timestamp': timezone.now().isoformat(),
        'stats': _stats_payload(),
        'video': video,
        'video_runtime': {
            'wvp': video.get('wvp', {}).get('runtime', {}),
            'zlm': video.get('zlm', {}).get('probe', {}),
        },
        'ports': PORTS_PAYLOAD,
        'latest_telemetry': TelemetrySerializer(latest_telemetry, many=True).data,
    })


@api_view(['GET'])
def home_dashboard(request):
    latest_telemetry = Telemetry.objects.select_related('gateway', 'device').order_by('-collected_at', '-created_at')[:10]
    latest_data = TelemetrySerializer(latest_telemetry, many=True).data

    gateway_summary = {
        'total': Gateway.objects.count(),
        'online': Gateway.objects.filter(status='online').count(),
        'by_status': list(Gateway.objects.values('status').annotate(count=Count('id')).order_by('status')),
    }

    device_summary = {
        'total': Device.objects.count(),
        'by_protocol': list(Device.objects.values('protocol').annotate(count=Count('id')).order_by('protocol')),
        'by_status': list(Device.objects.values('status').annotate(count=Count('id')).order_by('status')),
        'by_type': list(Device.objects.values('device_type').annotate(count=Count('id')).order_by('device_type')),
    }

    telemetry_summary_payload = {
        'total': Telemetry.objects.count(),
        'latest_count': len(latest_data),
    }

    video = _video_status_payload()
    return Response({
        'status': 'ok',
        'timestamp': timezone.now().isoformat(),
        'stats': _stats_payload(),
        'video': video,
        'video_runtime': {
            'wvp': video.get('wvp', {}).get('runtime', {}),
            'zlm': video.get('zlm', {}).get('probe', {}),
        },
        'ports': PORTS_PAYLOAD,
        'gateway_summary': gateway_summary,
        'device_summary': device_summary,
        'telemetry_summary': telemetry_summary_payload,
        'latest_telemetry': latest_data,
    })


@api_view(['GET'])
def gateways_summary(request):
    by_status = list(Gateway.objects.values('status').annotate(count=Count('id')).order_by('status'))
    return Response({
        'total': Gateway.objects.count(),
        'online': Gateway.objects.filter(status='online').count(),
        'by_status': by_status,
    })


@api_view(['GET'])
def devices_summary(request):
    by_protocol = list(Device.objects.values('protocol').annotate(count=Count('id')).order_by('protocol'))
    by_status = list(Device.objects.values('status').annotate(count=Count('id')).order_by('status'))
    by_type = list(Device.objects.values('device_type').annotate(count=Count('id')).order_by('device_type'))

    return Response({
        'total': Device.objects.count(),
        'by_protocol': by_protocol,
        'by_status': by_status,
        'by_type': by_type,
    })


@api_view(['GET'])
def telemetry_summary(request):
    latest_telemetry = Telemetry.objects.select_related('gateway', 'device').order_by('-collected_at', '-created_at')[:10]
    latest_data = TelemetrySerializer(latest_telemetry, many=True).data

    return Response({
        'total': Telemetry.objects.count(),
        'latest_count': len(latest_data),
        'latest': latest_data,
    })


def index(request):
    return JsonResponse({
        'message': 'RK3576 Edge Platform Django API is running',
        'api_health': '/api/health/',
        'overview': '/api/overview/',
        'video_status': '/api/video/status/',
        'system_ports': '/api/system/ports/',
        'system_status': '/api/system/status/',
        'home_dashboard': '/api/home/dashboard/',
        'gateways_summary': '/api/gateways/summary/',
        'devices_summary': '/api/devices/summary/',
        'telemetry_summary': '/api/telemetry/summary/',
        'gateways': '/api/gateways/',
        'devices': '/api/devices/',
        'telemetry': '/api/telemetry/',
    })


@api_view(['GET', 'POST'])
def gateway_list_create(request):
    if request.method == 'GET':
        queryset = Gateway.objects.annotate(device_count=Count('devices')).all().order_by('-created_at')

        status_filter = request.GET.get('status')
        serial_number = request.GET.get('serial_number')
        q = request.GET.get('q')
        limit = _parse_int(request.GET.get('limit'), default=100, minimum=1, maximum=500)

        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if serial_number:
            queryset = queryset.filter(serial_number=serial_number)
        if q:
            queryset = queryset.filter(name__icontains=q) | queryset.filter(serial_number__icontains=q)

        serializer = GatewaySerializer(queryset[:limit], many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
        })

    serializer = GatewaySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def gateway_detail(request, pk):
    try:
        gateway = Gateway.objects.get(pk=pk)
    except Gateway.DoesNotExist:
        return Response({'detail': 'Gateway not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = GatewaySerializer(gateway)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def device_list_create(request):
    if request.method == 'GET':
        queryset = Device.objects.select_related('gateway').all().order_by('-created_at')

        gateway_id = request.GET.get('gateway')
        status_filter = request.GET.get('status')
        protocol = request.GET.get('protocol')
        device_type = request.GET.get('device_type')
        q = request.GET.get('q')
        limit = _parse_int(request.GET.get('limit'), default=100, minimum=1, maximum=500)

        if gateway_id:
            queryset = queryset.filter(gateway_id=gateway_id)
        if status_filter:
            queryset = queryset.filter(status=status_filter)
        if protocol:
            queryset = queryset.filter(protocol=protocol)
        if device_type:
            queryset = queryset.filter(device_type=device_type)
        if q:
            queryset = queryset.filter(name__icontains=q) | queryset.filter(device_id__icontains=q)

        serializer = DeviceSerializer(queryset[:limit], many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
        })

    serializer = DeviceSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def device_detail(request, pk):
    try:
        device = Device.objects.select_related('gateway').get(pk=pk)
    except Device.DoesNotExist:
        return Response({'detail': 'Device not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = DeviceSerializer(device)
    return Response(serializer.data)


@api_view(['GET', 'POST'])
def telemetry_list_create(request):
    if request.method == 'GET':
        queryset = Telemetry.objects.select_related('gateway', 'device').all().order_by('-collected_at', '-created_at')

        gateway_id = request.GET.get('gateway')
        device_id = request.GET.get('device')
        topic = request.GET.get('topic')
        limit = _parse_int(request.GET.get('limit'), default=100, minimum=1, maximum=1000)

        if gateway_id:
            queryset = queryset.filter(gateway_id=gateway_id)
        if device_id:
            queryset = queryset.filter(device_id=device_id)
        if topic:
            queryset = queryset.filter(topic__icontains=topic)

        serializer = TelemetrySerializer(queryset[:limit], many=True)
        return Response({
            'count': queryset.count(),
            'results': serializer.data,
        })

    serializer = TelemetrySerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['GET'])
def telemetry_detail(request, pk):
    try:
        telemetry = Telemetry.objects.select_related('gateway', 'device').get(pk=pk)
    except Telemetry.DoesNotExist:
        return Response({'detail': 'Telemetry not found'}, status=status.HTTP_404_NOT_FOUND)

    serializer = TelemetrySerializer(telemetry)
    return Response(serializer.data)
