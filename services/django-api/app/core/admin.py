from django.contrib import admin

from .models import Device, Gateway, PlatformUser, Telemetry


@admin.register(Gateway)
class GatewayAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'serial_number', 'status', 'ip_address', 'updated_at')
    search_fields = ('name', 'serial_number')
    list_filter = ('status',)


@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display = ('id', 'name', 'device_id', 'device_type', 'protocol', 'status', 'gateway')
    search_fields = ('name', 'device_id')
    list_filter = ('protocol', 'status', 'device_type')


@admin.register(Telemetry)
class TelemetryAdmin(admin.ModelAdmin):
    list_display = ('id', 'device', 'gateway', 'topic', 'collected_at', 'created_at')
    search_fields = ('topic', 'device__device_id', 'gateway__serial_number')
    list_filter = ('gateway', 'device')


@admin.register(PlatformUser)
class PlatformUserAdmin(admin.ModelAdmin):
    list_display = ('id', 'username', 'display_name', 'role', 'is_active', 'last_login_at', 'updated_at')
    search_fields = ('username', 'display_name')
    list_filter = ('role', 'is_active')
