# gateway-core 骨架说明

当前已提供 `gateway-core` 开发骨架，用于未来接入：

- RS485 / RS232
- Modbus RTU / Modbus TCP
- 自定义串口协议
- 本地协议解析后转 MQTT

## 当前文件

- `services/gateway-core/main.py`
- `services/gateway-core/Dockerfile`
- `services/gateway-core/config.example.json`

## 当前行为

- 定时发布一条演示消息到 MQTT
- Django 自动订阅并写入数据库

## 后续建议

1. 增加真实串口读取逻辑
2. 增加配置文件加载
3. 增加多设备协议适配
4. 增加断线重连与本地缓存
