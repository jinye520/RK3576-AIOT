import json
import os
import time
from datetime import datetime, timezone

import paho.mqtt.client as mqtt

MQTT_HOST = os.getenv('MQTT_HOST', 'mqtt')
MQTT_PORT = int(os.getenv('MQTT_PORT', '1883'))
TOPIC = 'edge/RK3576-0001/sensor/gateway-core-demo/up'


def build_payload():
    return {
        'gateway_sn': 'RK3576-0001',
        'gateway_name': 'RK3576 Gateway',
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
            'source': 'gateway-core'
        }
    }


def main():
    client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)
    client.connect(MQTT_HOST, MQTT_PORT, 60)
    client.loop_start()
    print(f'[gateway-core] connected to {MQTT_HOST}:{MQTT_PORT}')

    while True:
        payload = build_payload()
        client.publish(TOPIC, json.dumps(payload, ensure_ascii=False))
        print(f'[gateway-core] published to {TOPIC}')
        time.sleep(30)


if __name__ == '__main__':
    main()
