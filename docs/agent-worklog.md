# RK3576 AIOT Agent Worklog

> 记录本项目在当前阶段由智能编码代理持续推进的关键需求、实现过程、验证结果与 Git 提交，便于后续追溯、交接与演示。

## 项目信息
- 项目目录：`/home/snow/RK3576-AIOT`
- GitHub 仓库：`https://github.com/jinye520/RK3576-AIOT.git`
- 目标平台：当前 WSL Ubuntu 开发，后续迁移 RK3576 ARM64
- 核心栈：`MQTT + Node-RED + Django + Vue(静态 dist 原型) + Docker + WVP-GB28181-pro + ZLMediaKit`

---

## 一、基础平台原型阶段

### 目标
搭建可运行的边缘物联网平台原型，打通设备采集、消息总线、后端入库和前端可视化。

### 主要实现
- 初始化 Git 仓库、建立 `.gitignore`、切换到 `main`
- 创建 Docker Compose 拆分编排：
  - `docker-compose.base.yml`
  - `docker-compose.video.yml`
  - `docker-compose.devtools.yml`
- 新增脚本与 Makefile：
  - `scripts/start-base.sh`
  - `scripts/start-video.sh`
  - `scripts/start-all.sh`
  - `scripts/stop-all.sh`
  - `scripts/status.sh`
  - `scripts/logs-base.sh`
  - `scripts/logs-all.sh`
  - `Makefile`
- 因宿主机端口冲突，统一改用非默认端口：
  - Nginx `8088`
  - Django `8008`
  - Node-RED `1888`
  - MySQL `13316`
  - Redis `16380`
  - MQTT `11883`

### 结果
基础平台容器可运行并形成最小演示环境。

---

## 二、Django 中台与 MQTT 自动入库阶段

### 目标
让 Django 承担平台中台角色，形成网关、设备、遥测数据模型，并打通 MQTT 自动入库。

### 主要实现
- 创建 Django 项目结构：`services/django-api/app/`
- 新增模型：
  - `Gateway`
  - `Device`
  - `Telemetry`
- 新增 API：
  - `/api/`
  - `/api/health/`
  - `/api/overview/`
  - `/api/gateways/`
  - `/api/gateways/summary/`
  - `/api/devices/`
  - `/api/devices/summary/`
  - `/api/telemetry/`
  - `/api/telemetry/summary/`
- 新增 MQTT 自动订阅与写库：
  - 文件：`services/django-api/app/core/mqtt_client.py`
  - 主题：`edge/+/sensor/+/up`
- 在 `core/apps.py` 的 `ready()` 中启动 MQTT 监听
- 打通 `Node-RED -> MQTT -> Django -> MySQL`

### 结果
平台具备自动建档与自动接收遥测数据能力。

---

## 三、首页总览页面阶段

### 目标
快速形成可演示的前端总览页，不先引入正式 Vue 工程，而用静态 `dist` 页面承载实时展示。

### 主要实现
- 升级首页：`services/vue-web/dist/index.html`
- 首页接入 Django 聚合接口数据，展示：
  - 统计卡片
  - 最新遥测
  - 系统端口入口
  - 视频状态摘要
- 新增文档：
  - `docs/homepage-roadmap.md`
  - `docs/dashboard-api.md`
  - `docs/system-api.md`

### 结果
首页可作为平台实时总览与演示入口。

---

## 四、视频子系统真实接入阶段（WVP + ZLM）

### 目标
将视频能力从骨架推进为真实 WVP-GB28181-pro + ZLMediaKit 接入闭环。

### 主要实现
- 接入官方 WVP 源码：`/tmp/wvp-GB28181-pro`
- 使用 builder 自动构建：
  - `data/wvp/wvp-pro.jar`
  - `data/wvp/runtime-override/static/`
- 新增/调整文件：
  - `docker/wvp/start-wvp.sh`
  - `docker/wvp/application-docker.yml`
  - `docker/zlm/config.ini`
  - `docker-compose.video.yml`
- 修复 WVP 与 ZLM secret 不一致问题：
  - 统一 `ZLM_SERCERT=0`
- 恢复 WVP 前端静态资源入口：
  - `http://localhost:28080/`
  - `http://localhost:28080/#/login`
- 验证：
  - WVP 登录 API 可用
  - 媒体节点在线
  - Swagger / Knife4j 文档可访问
  - 冷启动可自动建表

### 结果
WVP/ZLM 真实运行，视频子系统不再只是占位。

---

## 五、视频聚合接口与首页视频化阶段

### 目标
将视频运行态与资源摘要纳入 Django 聚合接口与首页展示。

### 主要实现
- `services/django-api/app/core/views.py` 中新增：
  - `_wvp_login_token()`
  - `_video_inventory_payload()`
  - `_video_status_payload()`
- 新增接口：
  - `/api/video/status/`
  - `/api/video/runtime/`
  - `/api/video/inventory/`
  - `/api/video/bigscreen/`
- 将 `video_runtime`、`video_inventory` 嵌入：
  - `/api/overview/`
  - `/api/system/status/`
  - `/api/home/dashboard/`
- 首页增加：
  - 视频运行态面板
  - 视频资源摘要面板
  - WVP 与视频入口

### 结果
首页从纯物联页演进为“物联 + 视频”双栈总览页。

---

## 六、指挥大屏阶段

### 目标
增加大屏展示页面，集中呈现视频矩阵、传感器曲线、最新遥测流和视频资源摘要。

### 主要实现
- 新增页面：`services/vue-web/dist/bigscreen.html`
- 首页增加大屏入口：`/bigscreen.html`
- 新增大屏专用接口：`GET /api/video/bigscreen/`
- 大屏展示内容：
  - 顶部总览指标
  - 平台运行状态
  - 传感器数据趋势曲线
  - 最新遥测流
  - 视频资源摘要
  - 视频监控矩阵
- 增加动态视频槽位：
  - `BIGSCREEN_VIDEO_SLOTS`
  - 返回 `name / channel / stream_url / player_url / status / tag`

### 当前状态
- 视频矩阵已动态渲染
- 当前仍以动态槽位/跳转入口为主
- 尚未接入真实播放器流位

---

## 七、平台登录与角色菜单阶段

### 背景
新增诉求：
- 增加登录页面
- 实现账户管理
- 根据不同角色显示不同菜单

### 决策
采用“平台首页自己的登录体系”，不接管 WVP 原生登录。

### 主要实现
#### 1. 平台用户模型
文件：`services/django-api/app/core/models.py`

新增模型：`PlatformUser`
- 字段：
  - `username`
  - `password_hash`
  - `display_name`
  - `role`
  - `is_active`
  - `last_login_at`
- 角色：
  - `admin`
  - `operator`
  - `viewer`
- 内置菜单映射：
  - `admin`: dashboard / bigscreen / telemetry / devices / gateways / video / nodered / users / system
  - `operator`: dashboard / bigscreen / telemetry / devices / gateways / video / nodered
  - `viewer`: dashboard / bigscreen / telemetry / video

#### 2. 序列化与后台管理
- `PlatformUserSerializer`
- `PlatformUserCreateSerializer`
- 在 Django Admin 中注册：
  - `Gateway`
  - `Device`
  - `Telemetry`
  - `PlatformUser`

#### 3. 登录与会话接口
新增接口：
- `GET /api/platform/session/`
- `POST /api/platform/login/`
- `POST /api/platform/logout/`

#### 4. 默认账户种子
自动生成默认账号：
- `admin / admin123456`
- `operator / operator123`
- `viewer / viewer123`

#### 5. 平台登录页
页面：`services/vue-web/dist/login.html`
地址：`http://localhost:8088/login.html`

已支持：
- 登录
- 查看账户列表
- 创建测试账户
- 登录后展示角色菜单

#### 6. 首页角色联动
页面：`services/vue-web/dist/index.html`

已增加：
- 登录态展示
- 当前用户信息
- 退出登录
- 部分入口按角色菜单动态隐藏

#### 7. 大屏登录态联动
页面：`services/vue-web/dist/bigscreen.html`

已增加：
- 大屏登录态提示
- 演示模式/已登录说明

---

## 八、用户管理页阶段

### 目标
实现管理员可用的账户管理页。

### 页面
- `services/vue-web/dist/users.html`
- 地址：`http://localhost:8088/users.html`

### 后端能力
新增/增强接口：
- `GET /api/platform/users/`
  - 仅管理员可访问
  - 支持 `role` 与 `keyword` 过滤
- `POST /api/platform/users/create/`
  - 仅管理员可访问
- `GET /api/platform/users/<id>/`
  - 仅管理员可访问
- `PATCH /api/platform/users/<id>/`
  - 仅管理员可访问
- `POST /api/platform/users/<id>/reset-password/`
  - 仅管理员可访问
- `DELETE /api/platform/users/<id>/`
  - 仅管理员可访问
  - 禁止删除当前登录管理员自己

### 前端能力
用户管理页支持：
- 账户列表
- 角色筛选
- 关键字搜索
- 创建账户
- 修改显示名/用户名/角色/启停状态
- 重置密码
- 删除账户
- 删除二次确认
- 账户结构统计：
  - 总数
  - admin 数量
  - operator 数量
  - viewer 数量

### 结果
平台已形成一套最小可用的 RBAC 原型闭环。

---

## 九、相关页面与入口

### 平台入口
- 首页：`http://localhost:8088/`
- 平台登录页：`http://localhost:8088/login.html`
- 用户管理页：`http://localhost:8088/users.html`
- 指挥大屏：`http://localhost:8088/bigscreen.html`
- API 入口：`http://localhost:8008/api/`

### 视频入口
- WVP 后台：`http://localhost:28080/`
- WVP 登录页：`http://localhost:28080/#/login`
- WVP Knife4j：`http://localhost:28080/doc.html`
- WVP Swagger UI：`http://localhost:28080/swagger-ui/index.html`
- ZLM HTTP：`http://localhost:28082`

---

## 十、关键验证结果

### 登录与账户管理
- `viewer / viewer123` 可登录
- `admin / admin123456` 可登录并访问用户管理
- 可成功创建测试用户
- 可成功修改角色与启停状态
- 可成功重置密码
- 可成功删除普通账户
- 删除当前 admin 自己会被阻止

### 视频能力
- WVP 登录 API 可用
- 媒体节点在线
- 文档可访问
- 前端恢复成功

### 大屏能力
- 大屏 API 可返回视频槽位与遥测流
- 大屏可显示视频矩阵、曲线与资源摘要

---

## 十一、近期相关 Git 提交

> 以下为当前阶段关键提交摘要，完整记录以 `git log --oneline` 为准。

- `feat: add platform login and role-based menus`
- `feat: apply role-aware session menus on dashboard`
- `feat: add admin user management page`
- `feat: add user deletion and summary stats`

---

## 十二、当前遗留与后续建议

### 仍待完善
- 首页尚未升级为正式后台左侧导航布局
- 大屏视频矩阵尚未接入真实流播放位
- `channel_total` 等视频资源统计仍需打通真实接口
- 用户管理尚未提供删除保护以外的审计日志
- 尚未加入更细粒度权限点控制

### 建议下一步
1. 将首页升级为后台式布局：左侧菜单 + 顶部用户区 + 主内容区
2. 把角色控制从“入口隐藏”扩展为完整导航控制
3. 为用户管理增加操作审计日志
4. 为视频矩阵接入真实播放器/流地址
5. 将静态 `dist` 页逐步迁移为正式 Vue 工程

---

## 十三、如何查看历史

### 看代码变更
```bash
git log --oneline
git show <commit-id>
```

### 看本文档
```bash
less docs/agent-worklog.md
```

### 看接口
- `http://localhost:8008/api/`
- `http://localhost:28080/doc.html`

---

## 十四、说明
本文件属于“需求-实现-验证”层面的工作日志，和 Git 提交历史互补：
- Git 负责记录代码差异
- 本文档负责记录为什么做、做了什么、现在到哪一步

建议后续继续在每个大阶段更新本文件。
