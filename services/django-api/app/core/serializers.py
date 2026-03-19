from rest_framework import serializers

from .models import Device, Gateway, Telemetry


class GatewaySerializer(serializers.ModelSerializer):
    class Meta:
        model = Gateway
        fields = '__all__'


class DeviceSerializer(serializers.ModelSerializer):
    class Meta:
        model = Device
        fields = '__all__'


class TelemetrySerializer(serializers.ModelSerializer):
    class Meta:
        model = Telemetry
        fields = '__all__'
