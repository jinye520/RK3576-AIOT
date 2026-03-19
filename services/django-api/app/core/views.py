from django.db.models import Count
from django.http import JsonResponse
from django.utils import timezone
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response

from .models import Device, Gateway, Telemetry
from .serializers import DeviceSerializer, GatewaySerializer, TelemetrySerializer


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

    stats = {
        'gateway_count': Gateway.objects.count(),
        'device_count': Device.objects.count(),
        'telemetry_count': Telemetry.objects.count(),
        'online_gateway_count': Gateway.objects.filter(status='online').count(),
        'online_device_count': Device.objects.filter(status='online').count(),
    }

    return Response({
        'stats': stats,
        'latest_telemetry': latest_data,
    })


def index(request):
    return JsonResponse({
        'message': 'RK3576 Edge Platform Django API is running',
        'api_health': '/api/health/',
        'overview': '/api/overview/',
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
