# WVP Placeholder

当前 `docker-compose.video.yml` 中的 `wvp` 服务为占位容器，用于先完成视频子系统网络、端口、卷、配置结构搭建。

## 下一步接入真实 WVP-GB28181-pro

建议后续补充：

1. 下载并放置 WVP 可运行包/JAR 到 `data/wvp/`
2. 将 `docker-compose.video.yml` 中的 `wvp` 服务改为真实启动命令
3. 根据实际版本完善 `application-docker.yml`
4. 初始化 WVP 数据库
5. 联调 ZLMediaKit、SIP、RTP、录像目录

## 推荐后续结构

```text
data/wvp/
├── wvp-pro.jar
├── logs/
└── config/
```
