# Node-RED 演示流说明

已提供可直接导入的演示流文件：

- `flows/node-red-mqtt-demo.json`

## 用途

- 每 5 秒生成一次模拟温湿度数据
- 通过 MQTT 发布到：

```text
edge/RK3576-0001/sensor/sensor-demo-001/up
```

- Django 自动订阅并写入数据库
- 首页与 `/api/telemetry/` 可直接查看效果

## 导入方法

1. 打开 Node-RED：`http://localhost:1888/`
2. 右上角菜单 -> Import
3. 选择 `flows/node-red-mqtt-demo.json`
4. Deploy

## 验证方法

- 查看首页：`http://localhost:8088/`
- 查看概览：`http://localhost:8008/api/overview/`
- 查看遥测：`http://localhost:8008/api/telemetry/`
