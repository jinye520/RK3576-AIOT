import json
import os
import threading
import time
from datetime import datetime

import paho.mqtt.client as mqtt
from django.apps import apps
from django.db import close_old_connections
from django.utils import timezone
from django.utils.dateparse import parse_datetime

_started = False
_lock = threading.Lock()
_client = None


MQTT_HOST = os.getenv('MQTT_HOST', 'mqtt')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
MQTT_TOPIC = os.getenv('MQTT_TOPIC', 'edge/+/sensor/+/up')


def _parse_collected_at(value):
    if not value:
        return timezone.now()

    if isinstance(value, datetime):
        dt = value
    else:
        dt = parse_datetime(str(value))
        if dt is None:
            return timezone.now()

    if timezone.is_naive(dt):
        return timezone.make_aware(dt, timezone.get_current_timezone())
    return dt


def _extract_gateway_serial(topic_parts, payload):
    if len(topic_parts) > 1 and topic_parts[0] == 'edge':
        return topic_parts[1]
    return payload.get('gateway_sn') or payload.get('gateway_serial') or 'unknown-gateway'


def _extract_device_id(topic_parts, payload):
    if len(topic_parts) > 3:
        return topic_parts[3]
    return payload.get('device_id') or 'unknown-device'


def _extract_device_type(payload):
    return payload.get('device_type') or payload.get('type') or 'unknown'


def _extract_protocol(payload):
    protocol = payload.get('protocol', 'mqtt')
    valid_protocols = {'modbus_rtu', 'modbus_tcp', 'mqtt', 'gb28181', 'custom'}
    return protocol if protocol in valid_protocols else 'custom'


def _extract_status(payload):
    return payload.get('status', 'online')


def _extract_telemetry_payload(payload):
    if isinstance(payload.get('data'), dict):
        return payload['data']
    return payload.get('payload', payload)


def _save_message(topic, payload):
    close_old_connections()

    Gateway = apps.get_model('core', 'Gateway')
    Device = apps.get_model('core', 'Device')
    Telemetry = apps.get_model('core', 'Telemetry')

    topic_parts = topic.split('/')
    gateway_serial = _extract_gateway_serial(topic_parts, payload)
    device_id = _extract_device_id(topic_parts, payload)

    gateway_defaults = {
        'name': payload.get('gateway_name') or gateway_serial,
        'ip_address': payload.get('gateway_ip'),
        'status': _extract_status(payload),
        'description': payload.get('gateway_description', 'Auto created from MQTT'),
    }
    gateway, _ = Gateway.objects.get_or_create(
        serial_number=gateway_serial,
        defaults=gateway_defaults,
    )

    gateway_updated = False
    for field, value in gateway_defaults.items():
        if value and getattr(gateway, field) != value:
            setattr(gateway, field, value)
            gateway_updated = True
    if gateway_updated:
        gateway.save(update_fields=['name', 'ip_address', 'status', 'description', 'updated_at'])

    device_defaults = {
        'name': payload.get('device_name') or device_id,
        'device_type': _extract_device_type(payload),
        'protocol': _extract_protocol(payload),
        'status': _extract_status(payload),
        'metadata': payload.get('metadata', {}),
    }
    device, _ = Device.objects.get_or_create(
        gateway=gateway,
        device_id=device_id,
        defaults=device_defaults,
    )

    device_updated = False
    for field, value in device_defaults.items():
        if value and getattr(device, field) != value:
            setattr(device, field, value)
            device_updated = True
    if device_updated:
        device.save(update_fields=['name', 'device_type', 'protocol', 'status', 'metadata', 'updated_at'])

    Telemetry.objects.create(
        gateway=gateway,
        device=device,
        topic=topic,
        payload=_extract_telemetry_payload(payload),
        collected_at=_parse_collected_at(payload.get('timestamp') or payload.get('collected_at')),
    )


def _on_connect(client, userdata, flags, reason_code, properties=None):
    try:
        client.subscribe(MQTT_TOPIC)
        print(f'[MQTT] subscribed to {MQTT_TOPIC}')
    except Exception as exc:
        print(f'[MQTT] subscribe failed: {exc}')


def _on_message(client, userdata, msg):
    try:
        payload = json.loads(msg.payload.decode('utf-8'))
    except Exception as exc:
        print(f'[MQTT] invalid JSON on {msg.topic}: {exc}')
        return

    try:
        _save_message(msg.topic, payload)
        print(f'[MQTT] stored telemetry from topic={msg.topic}')
    except Exception as exc:
        print(f'[MQTT] failed to store message from {msg.topic}: {exc}')


def _run_client():
    global _client

    while True:
        try:
            client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
            client.on_connect = _on_connect
            client.on_message = _on_message
            client.connect(MQTT_HOST, MQTT_PORT, 60)
            _client = client
            print(f'[MQTT] connected to {MQTT_HOST}:{MQTT_PORT}')
            client.loop_forever()
        except Exception as exc:
            print(f'[MQTT] connection error: {exc}; retrying in 5 seconds')
            time.sleep(5)


def start_mqtt_listener():
    global _started

    with _lock:
        if _started:
            return
        _started = True

    thread = threading.Thread(target=_run_client, daemon=True)
    thread.start()
    print('[MQTT] listener thread started')
