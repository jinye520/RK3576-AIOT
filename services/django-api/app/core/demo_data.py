PORTS_PAYLOAD = {
    'web': {
        'homepage': 'http://localhost:8088/',
        'api': 'http://localhost:8008/api/',
        'api_health': 'http://localhost:8008/api/health/',
        'api_overview': 'http://localhost:8008/api/overview/',
        'video_status': 'http://localhost:8008/api/video/status/',
        'node_red_proxy': 'http://localhost:8088/nodered/',
    },
    'services': {
        'node_red': {
            'host': 'localhost',
            'port': 1888,
            'url': 'http://localhost:1888/',
        },
        'mqtt': {
            'tcp_host': 'localhost',
            'tcp_port': 11883,
            'ws_port': 19001,
        },
        'mysql': {
            'host': 'localhost',
            'port': 13316,
        },
        'redis': {
            'host': 'localhost',
            'port': 16380,
        },
        'zlm': {
            'http_url': 'http://localhost:28082',
            'https_url': 'https://localhost:28443',
            'rtsp_port': 15540,
            'rtmp_port': 19350,
            'rtc_port': 11000,
        },
        'wvp': {
            'http_url': 'http://localhost:28080',
            'sip_tcp_port': 25060,
            'sip_udp_port': 15060,
            'rtp_udp_range': '13000-13100',
        },
    },
}
