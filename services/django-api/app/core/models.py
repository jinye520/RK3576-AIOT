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
