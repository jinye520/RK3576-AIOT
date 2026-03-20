from django.contrib.auth.hashers import make_password
from django.db import models


class TimestampedModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True


class Gateway(TimestampedModel):
    name = models.CharField(max_length=100)
    serial_number = models.CharField(max_length=100, unique=True)
    ip_address = models.GenericIPAddressField(blank=True, null=True)
    status = models.CharField(max_length=20, default='offline')
    description = models.TextField(blank=True, default='')

    def __str__(self):
        return f"{self.name} ({self.serial_number})"


class Device(TimestampedModel):
    PROTOCOL_CHOICES = [
        ('modbus_rtu', 'Modbus RTU'),
        ('modbus_tcp', 'Modbus TCP'),
        ('mqtt', 'MQTT'),
        ('gb28181', 'GB28181'),
        ('custom', 'Custom'),
    ]

    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='devices')
    name = models.CharField(max_length=100)
    device_id = models.CharField(max_length=100)
    device_type = models.CharField(max_length=50)
    protocol = models.CharField(max_length=30, choices=PROTOCOL_CHOICES, default='custom')
    status = models.CharField(max_length=20, default='offline')
    metadata = models.JSONField(default=dict, blank=True)

    class Meta:
        unique_together = ('gateway', 'device_id')

    def __str__(self):
        return f"{self.name} [{self.device_id}]"


class Telemetry(TimestampedModel):
    gateway = models.ForeignKey(Gateway, on_delete=models.CASCADE, related_name='telemetry')
    device = models.ForeignKey(Device, on_delete=models.CASCADE, related_name='telemetry')
    topic = models.CharField(max_length=255, blank=True, default='')
    payload = models.JSONField(default=dict)
    collected_at = models.DateTimeField()

    def __str__(self):
        return f"Telemetry<{self.device.device_id}@{self.collected_at}>"


class PlatformUser(TimestampedModel):
    ROLE_ADMIN = 'admin'
    ROLE_OPERATOR = 'operator'
    ROLE_VIEWER = 'viewer'

    ROLE_CHOICES = [
        (ROLE_ADMIN, '管理员'),
        (ROLE_OPERATOR, '运维员'),
        (ROLE_VIEWER, '观察员'),
    ]

    username = models.CharField(max_length=64, unique=True)
    password_hash = models.CharField(max_length=255)
    display_name = models.CharField(max_length=100)
    role = models.CharField(max_length=20, choices=ROLE_CHOICES, default=ROLE_VIEWER)
    is_active = models.BooleanField(default=True)
    last_login_at = models.DateTimeField(blank=True, null=True)

    MENU_MAP = {
        ROLE_ADMIN: [
            'dashboard',
            'bigscreen',
            'telemetry',
            'devices',
            'gateways',
            'video',
            'nodered',
            'users',
            'system',
        ],
        ROLE_OPERATOR: [
            'dashboard',
            'bigscreen',
            'telemetry',
            'devices',
            'gateways',
            'video',
            'nodered',
        ],
        ROLE_VIEWER: [
            'dashboard',
            'bigscreen',
            'telemetry',
            'video',
        ],
    }

    def __str__(self):
        return f"{self.display_name}<{self.username}>"

    @property
    def menus(self):
        return self.MENU_MAP.get(self.role, self.MENU_MAP[self.ROLE_VIEWER])

    def set_password(self, raw_password):
        self.password_hash = make_password(raw_password)


class PlatformSetting(TimestampedModel):
    SETTING_BASE_CONFIG = 'base_config'
    SETTING_COLLECT_CONFIG = 'collect_config'
    SETTING_PROTOCOL_CONFIG = 'protocol_config'
    SETTING_VIDEO_CONFIG = 'video_config'
    SETTING_CLOUD_CONFIG = 'cloud_config'

    SETTING_KEY_CHOICES = [
        (SETTING_BASE_CONFIG, '基础配置'),
        (SETTING_COLLECT_CONFIG, '数据采集配置'),
        (SETTING_PROTOCOL_CONFIG, '协议转换配置'),
        (SETTING_VIDEO_CONFIG, '视频接入配置'),
        (SETTING_CLOUD_CONFIG, '云平台推送配置'),
    ]

    key = models.CharField(max_length=64, unique=True, choices=SETTING_KEY_CHOICES)
    value = models.JSONField(default=dict, blank=True)
    updated_by = models.CharField(max_length=64, blank=True, default='')

    def __str__(self):
        return f"{self.key}<{self.updated_by or 'system'}>"
