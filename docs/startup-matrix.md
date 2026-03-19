# 启动矩阵说明

## 1. 基础平台

```bash
make base-up
```

包含：
- nginx
- vue-web
- django-api
- mysql
- redis
- mqtt
- node-red

## 2. 视频子系统

```bash
make video-up
```

包含：
- zlm
- wvp（当前为占位/骨架模式）

## 3. 开发工具骨架

```bash
make devtools-up
```

包含：
- gateway-core

## 4. 全部启动

```bash
make all-up
```

## 5. 查看状态

```bash
make ps
./scripts/status.sh
```

## 6. 停止全部

```bash
make down
```
