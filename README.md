# RK3576-AIOT

基于 RK3576 的物联网边缘计算平台原型，当前采用 Docker 容器化方式在 WSL Ubuntu 开发，后续可迁移部署到 RK3576 ARM64 设备。

当前基础能力包括：

- Django 后端 API
- Vue 前端占位页
- MQTT Broker（Mosquitto）
- Node-RED 在线编程
- MySQL
- Redis
- Nginx 统一入口
- Django 自动订阅 MQTT 并写入遥测数据

---

## 一、项目目标

本项目面向 RK3576 边缘设备，计划逐步集成以下能力：

- 摄像机接入、推流、本地录制、回放
- 串口传感器接入与协议解析
- Node-RED 在线编程与协议转换
- MQTT 消息总线
- Vue + Django 平台管理界面
- Docker 容器化部署
- 后续接入 WVP-GB28181-pro 与 ZLMediaKit

---

## 二、当前目录结构

```text
RK3576-AIOT/
├── README.md
├── .env.example
├── .gitignore
├── docker-compose.base.yml
├── docker/
│   ├── mosquitto/
│   │   └── mosquitto.conf
│   └── nginx/
│       ├── nginx.conf
│       └── conf.d/
│           └── default.conf
├── data/
│   ├── django-media/
│   ├── mosquitto/
│   ├── mosquitto-log/
│   ├── mysql/
│   ├── nodered/
│   └── redis/
└── services/
    ├── django-api/
    │   ├── Dockerfile
    │   ├── entrypoint.sh
    │   ├── requirements.txt
    │   └── app/
    │       ├── manage.py
    │       ├── config/
    │       └── core/
    └── vue-web/
        ├── Dockerfile
        └── dist/
```

---

## 三、当前运行服务

通过 `docker-compose.base.yml` 可启动以下服务：

- `nginx`
- `vue-web`
- `django-api`
- `mysql`
- `redis`
- `mqtt`
- `node-red`

通过 `docker-compose.video.yml` 可追加启动视频子系统：

- `zlm`
- `wvp`（当前为占位容器，后续替换为真实 WVP-GB28181-pro）

---

## 四、端口说明

为避免与当前机器上其他项目冲突，已使用以下端口：

| 服务 | 地址 |
|---|---|
| 平台首页 | http://localhost:8088/ |
| Django API | http://localhost:8008/api/ |
| Django Health | http://localhost:8008/api/health/ |
| 平台概览 | http://localhost:8008/api/overview/ |
| Node-RED | http://localhost:1888/ |
| Nginx 代理 Node-RED | http://localhost:8088/nodered/ |
| MQTT TCP | localhost:11883 |
| MQTT WebSocket | localhost:19001 |
| MySQL | localhost:13316 |
| Redis | localhost:16380 |

---

## 五、快速启动

### 1. 复制环境变量

```bash
cp .env.example .env
```

### 2. 创建数据目录

```bash
mkdir -p \
  data/mysql \
  data/redis \
  data/mosquitto \
  data/mosquitto-log \
  data/nodered \
  data/django-media \
  data/zlm/www \
  data/record \
  data/wvp
```

### 3. 启动基础服务

```bash
docker compose --env-file .env -f docker-compose.base.yml up -d --build
```

### 4. 查看服务状态

```bash
docker compose -f docker-compose.base.yml ps
```

### 5. 查看日志

```bash
docker compose -f docker-compose.base.yml logs -f
```

### 6. 启动视频子系统

```bash
docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.video.yml up -d
```

也可以使用脚本：

```bash
chmod +x scripts/*.sh
./scripts/start-base.sh
./scripts/start-video.sh
```

---

## 六、当前 Django API

### 基础接口

- `GET /api/`
- `GET /api/health/`
- `GET /api/overview/`

### Gateway

- `GET /api/gateways/`
- `POST /api/gateways/`
- `GET /api/gateways/<id>/`

支持筛选参数：

- `status`
- `serial_number`
- `q`
- `limit`

### Device

- `GET /api/devices/`
- `POST /api/devices/`
- `GET /api/devices/<id>/`

支持筛选参数：

- `gateway`
- `status`
- `protocol`
- `device_type`
- `q`
- `limit`

### Telemetry

- `GET /api/telemetry/`
- `POST /api/telemetry/`
- `GET /api/telemetry/<id>/`

支持筛选参数：

- `gateway`
- `device`
- `topic`
- `limit`

---

## 七、MQTT 自动入库说明

Django 当前已实现最小 MQTT 订阅逻辑：

- 自动连接 MQTT Broker
- 订阅主题：`edge/+/sensor/+/up`
- 自动创建 Gateway / Device
- 自动写入 Telemetry

### 推荐 Topic 格式

```text
edge/{gateway_sn}/sensor/{device_id}/up
```

例如：

```text
edge/RK3576-0001/sensor/sensor-demo-001/up
```

### 推荐 Payload 格式

```json
{
  "gateway_sn": "RK3576-0001",
  "gateway_name": "RK3576 Gateway",
  "device_id": "sensor-demo-001",
  "device_name": "演示温湿度传感器",
  "device_type": "temperature_humidity",
  "protocol": "mqtt",
  "status": "online",
  "timestamp": "2026-03-20T01:00:00+08:00",
  "data": {
    "temperature": 25.8,
    "humidity": 62.1
  },
  "metadata": {
    "source": "node-red-demo",
    "port": "virtual"
  }
}
```

---

## 八、Node-RED 演示流思路

当前建议使用以下最小演示链路：

```text
inject -> function -> mqtt out
```

用途：

- 模拟传感器数据
- 周期性发布到 MQTT
- Django 自动接收并入库

推荐发布主题：

```text
edge/RK3576-0001/sensor/sensor-demo-001/up
```

---

## 九、开发阶段建议

### 第一阶段：基础平台

已完成：

- Docker 基础编排
- Django / Vue / MQTT / Node-RED / MySQL / Redis 启动
- 最小 API
- MQTT 自动入库

### 第二阶段：前端真实数据面板

待完成：

- 首页读取 `/api/overview/`
- 显示网关数、设备数、遥测数
- 显示最新遥测列表

### 第三阶段：串口采集接入

计划：

- 新增 `gateway-core`
- 接入 RS485 / Modbus RTU
- 协议解析后推送 MQTT

### 第四阶段：视频能力接入

当前已完成视频子系统骨架：

- `docker-compose.video.yml`
- `zlm` 服务编排
- `wvp` 占位容器
- ZLM 与 WVP 配置文件结构

后续计划：

- 替换为真实 WVP-GB28181-pro 服务
- 接入 ZLMediaKit 完整媒体链路
- 实现摄像机预览、录像、回放

---

## 十、后续规划

后续将逐步扩展：

- Vue 管理后台
- 用户与权限系统
- 设备管理页面
- 告警中心
- 时序数据展示
- WVP + ZLM 视频子系统
- 串口采集服务
- 多架构镜像（amd64 / arm64）
- RK3576 真机部署方案
- Django 对视频子系统的管理接口
- Vue 视频管理与预览页面

---

## 十一、注意事项

- `.env` 已被 `.gitignore` 忽略，请勿提交真实敏感配置
- 当前 Django 运行在开发服务器模式，后续应切换到 `gunicorn`
- WSL 下适合做基础联调，GB28181 / 串口 / ARM64 真机能力需在 RK3576 上进一步验证
- Mosquitto 当前为开发模式，生产环境建议启用认证与 ACL

---

## 十二、Git 仓库

GitHub：

- https://github.com/jinye520/RK3576-AIOT

## 十三、视频子系统文档

- `docs/video-subsystem.md`
