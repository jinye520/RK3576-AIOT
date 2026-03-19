# 视频子系统设计草案

本文件描述 RK3576-AIOT 平台的视频子系统第一版容器化设计。

## 目标

- 接入 WVP-GB28181-pro
- 接入 ZLMediaKit
- 为后续摄像机接入、实时预览、录像回放提供基础骨架

## 当前编排文件

- `docker-compose.video.yml`

## 当前服务

### zlm

使用镜像：

- `zlmediakit/zlmediakit:master`

当前用途：

- 提供 RTSP / RTMP / HTTP / WebRTC 媒体服务基础能力
- 提供录像目录卷挂载
- 预留后续 hook 与鉴权扩展

### wvp

当前为占位容器，用于先完成：

- 网络联通
- 端口规划
- 卷目录规划
- 配置文件结构规划

后续需要替换为真实 WVP 服务。

## 端口规划

| 服务 | 容器端口 | 宿主机端口 |
|---|---:|---:|
| ZLM HTTP | 80 | 28082 |
| ZLM HTTPS | 443 | 28443 |
| ZLM RTMP | 1935 | 19350 |
| ZLM RTSP | 554 | 15540 |
| ZLM RTC | 10000 | 11000 |
| WVP HTTP | 18080 | 28080 |
| WVP SIP TCP | 5060 | 25060 |
| WVP SIP UDP | 5060 | 25060/udp |
| WVP RTP UDP | 30000-30100 | 13000-13100/udp |

## 启动方式

先启动基础平台：

```bash
docker compose --env-file .env -f docker-compose.base.yml up -d --build
```

再启动视频子系统：

```bash
docker compose --env-file .env -f docker-compose.base.yml -f docker-compose.video.yml up -d
```

## 后续待实现

1. 将 WVP 占位容器替换为真实服务
2. 初始化 WVP 数据库
3. 增加 Nginx 视频代理入口
4. 增加 Django 对 WVP 的管理接口
5. 增加 Vue 视频管理页面
