from rest_framework import serializers

from .models import Device, Gateway, PlatformUser, Telemetry


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


class PlatformUserSerializer(serializers.ModelSerializer):
    menus = serializers.ListField(read_only=True)

    class Meta:
        model = PlatformUser
        fields = [
            'id',
            'username',
            'display_name',
            'role',
            'is_active',
            'last_login_at',
            'created_at',
            'updated_at',
            'menus',
        ]


class PlatformUserCreateSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, min_length=6)

    class Meta:
        model = PlatformUser
        fields = ['id', 'username', 'display_name', 'role', 'is_active', 'password']

    def validate_username(self, value):
        queryset = PlatformUser.objects.filter(username=value)
        if self.instance:
            queryset = queryset.exclude(pk=self.instance.pk)
        if queryset.exists():
            raise serializers.ValidationError('username already exists')
        return value

    def create(self, validated_data):
        password = validated_data.pop('password')
        user = PlatformUser(**validated_data)
        user.set_password(password)
        user.save()
        return user

    def update(self, instance, validated_data):
        password = validated_data.pop('password', None)
        for key, value in validated_data.items():
            setattr(instance, key, value)
        if password:
            instance.set_password(password)
        instance.save()
        return instance
