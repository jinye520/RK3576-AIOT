import argparse
import json
import os
import time
from datetime import datetime, timezone
from pathlib import Path

import paho.mqtt.client as mqtt

DEFAULT_CONFIG_PATH = Path('/app/config.json')
DEFAULT_TOPIC = 'edge/RK3576-0001/sensor/gateway-core-demo/up'


def load_config(config_path):
    if not config_path.exists():
        return {
            'gateway_sn': 'RK3576-0001',
            'gateway_name': 'RK3576 Gateway',
            'publish_interval_seconds': 30,
            'mqtt': {
                'host': os.getenv('MQTT_HOST', 'mqtt'),
                'port': int(os.getenv('MQTT_PORT', '1883')),
            },
            'serial': {
                'enabled': False,
                'port': '/dev/ttyUSB0',
                'baudrate': 9600,
                'protocol': 'modbus_rtu',
            },
            'demo': {
                'enabled': True,
                'topic': DEFAULT_TOPIC,
            },
        }

    with config_path.open('r', encoding='utf-8') as f:
        return json.load(f)


def build_payload(config):
    gateway_sn = config.get('gateway_sn', 'RK3576-0001')
    gateway_name = config.get('gateway_name', 'RK3576 Gateway')
    return {
        'gateway_sn': gateway_sn,
        'gateway_name': gateway_name,
        'device_id': 'gateway-core-demo',
        'device_name': 'Gateway Core Demo Sensor',
        'device_type': 'demo',
        'protocol': 'custom',
        'status': 'online',
        'timestamp': datetime.now(timezone.utc).isoformat(),
        'data': {
            'value': 1,
            'message': 'gateway-core skeleton running'
        },
        'metadata': {
            'source': 'gateway-core',
            'serial_enabled': config.get('serial', {}).get('enabled', False),
        }
    }


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--config', default=str(DEFAULT_CONFIG_PATH), help='Path to gateway-core config JSON')
    parser.add_argument('--demo', action='store_true', help='Force demo publishing mode')
    args = parser.parse_args()

    config_path = Path(args.config)
    config = load_config(config_path)

    mqtt_host = config.get('mqtt', {}).get('host', os.getenv('MQTT_HOST', 'mqtt'))
    mqtt_port = int(config.get('mqtt', {}).get('port', os.getenv('MQTT_PORT', '1883')))
    interval = int(config.get('publish_interval_seconds', 30))
    demo_topic = config.get('demo', {}).get('topic', DEFAULT_TOPIC)
    demo_enabled = args.demo or config.get('demo', {}).get('enabled', True)

    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(mqtt_host, mqtt_port, 60)
    client.loop_start()
    print(f'[gateway-core] connected to {mqtt_host}:{mqtt_port}')
    print(f'[gateway-core] config path: {config_path}')

    if not demo_enabled:
        print('[gateway-core] demo mode disabled; waiting for future serial implementation')
        while True:
            time.sleep(60)

    while True:
        payload = build_payload(config)
        client.publish(demo_topic, json.dumps(payload, ensure_ascii=False))
        print(f'[gateway-core] published to {demo_topic}')
        time.sleep(interval)


if __name__ == '__main__':
    main()
