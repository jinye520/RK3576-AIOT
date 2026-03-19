# RK3576 AIOT Change Timeline

> 按阶段整理本项目的重要演进节点，便于快速回看“什么时候做了什么、对应了什么能力、可从哪里进入”。

## 阶段 01：项目初始化与版本管理
- 初始化仓库并切换到 `main`
- 建立 `.gitignore`
- 建立与 GitHub 仓库的持续同步
- 仓库地址：`https://github.com/jinye520/RK3576-AIOT.git`

### 结果
项目具备可持续提交、回滚和协作的基础。

---

## 阶段 02：Docker 基础平台搭建
- 新增编排文件：
  - `docker-compose.base.yml`
  - `docker-compose.video.yml`
  - `docker-compose.devtools.yml`
- 新增启动/停止/日志脚本：
  - `scripts/start-base.sh`
  - `scripts/start-video.sh`
  - `scripts/start-all.sh`
  - `scripts/stop-all.sh`
  - `scripts/status.sh`
  - `scripts/logs-base.sh`
  - `scripts/logs-all.sh`
- 新增 `Makefile`

### 关键决策
由于宿主机已有其他项目占用默认端口，因此本项目统一改为避冲突端口。

### 对外入口
- 首页：`http://localhost:8088/`
- API：`http://localhost:8008/api/`
- Node-RED：`http://localhost:1888/`

---

## 阶段 03：Django 中台与物模型
- 建立 Django 项目：`services/django-api/app/`
- 新增模型：
  - `Gateway`
  - `Device`
  - `Telemetry`
- 新增 REST API：
  - `/api/health/`
  - `/api/overview/`
  - `/api/gateways/`
  - `/api/devices/`
  - `/api/telemetry/`
  - `/api/*/summary/`

### 结果
形成平台基础数据面。

---

## 阶段 04：MQTT 自动入库
- 新增：`services/django-api/app/core/mqtt_client.py`
- 在 `core/apps.py` 的 `ready()` 中启动 MQTT 监听
- 订阅主题：`edge/+/sensor/+/up`
- 自动创建网关/设备并写入遥测数据

### 结果
Node-RED 或其他上游发布 MQTT 后，Django 可自动建档并写 MySQL。

---

## 阶段 05：首页实时总览
- 升级：`services/vue-web/dist/index.html`
- 首页接入 `/api/overview/`
- 展示：
  - 网关数量
  - 设备数量
  - 遥测数量
  - 最新遥测
  - 平台入口
  - 系统端口

### 结果
形成可直接演示的静态前端总览页。

---

## 阶段 06：视频子系统骨架到真实接入
- 接入 WVP-GB28181-pro 官方工程
- 接入 ZLMediaKit
- 构建 builder 自动生成：
  - `data/wvp/wvp-pro.jar`
  - `data/wvp/runtime-override/static/`
- 修复 WVP / ZLM `secret` 不一致
- 恢复 WVP 前端静态页面

### 关键入口
- WVP 登录页：`http://localhost:28080/#/login`
- WVP 后台：`http://localhost:28080/`
- Knife4j：`http://localhost:28080/doc.html`
- Swagger UI：`http://localhost:28080/swagger-ui/index.html`
- ZLM：`http://localhost:28082`

### 结果
视频系统从“占位骨架”升级为真实可运行子系统。

---

## 阶段 07：视频聚合接口
- 新增：
  - `/api/video/status/`
  - `/api/video/runtime/`
  - `/api/video/inventory/`
  - `/api/video/bigscreen/`
- Django 开始主动探测：
  - WVP 可达性
  - ZLM 可达性
  - 登录可用性
  - admin 用户是否存在
  - 前端/文档是否可访问
  - 媒体节点数量

### 结果
视频状态不再只是“文件存在性判断”，而是带真实运行探测的聚合接口。

---

## 阶段 08：首页视频化
- 首页增加：
  - 视频运行态
  - 视频资源摘要
  - WVP 入口
  - 视频状态摘要卡片
- `/api/overview/`、`/api/system/status/`、`/api/home/dashboard/` 内嵌视频聚合结果

### 结果
首页成为物联 + 视频双栈总览页。

---

## 阶段 09：指挥大屏
- 新增页面：`services/vue-web/dist/bigscreen.html`
- 地址：`http://localhost:8088/bigscreen.html`
- 展示：
  - 顶部指标
  - 平台运行状态
  - 传感器曲线
  - 最新遥测流
  - 视频资源摘要
  - 视频矩阵
- 新增大屏专用 API：`/api/video/bigscreen/`

### 结果
形成指挥大屏原型。

---

## 阶段 10：大屏视频槽位动态化
- 在 Django 中增加 `BIGSCREEN_VIDEO_SLOTS`
- 大屏从 API 拉取 `video_slots`
- 每个槽位包括：
  - `name`
  - `channel`
  - `stream_url`
  - `player_url`
  - `status`
  - `tag`

### 当前状态
仍以动态槽位和跳转为主，尚未接入真实流播放器。

---

## 阶段 11：平台登录与角色菜单
- 新增自定义平台用户模型：`PlatformUser`
- 角色：
  - `admin`
  - `operator`
  - `viewer`
- 每个角色内置菜单权限映射
- 新增登录页：`http://localhost:8088/login.html`
- 新增 API：
  - `GET /api/platform/session/`
  - `POST /api/platform/login/`
  - `POST /api/platform/logout/`

### 默认账户
- `admin / admin123456`
- `operator / operator123`
- `viewer / viewer123`

### 结果
平台具备独立于 WVP 的登录体系。

---

## 阶段 12：首页登录态与角色菜单联动
- 首页新增登录态区块
- 显示当前用户、角色、菜单
- 增加退出登录
- 部分入口根据角色动态隐藏
- 大屏增加登录态说明

### 结果
“不同角色显示不同菜单”开始落到 UI 层。

---

## 阶段 13：管理员用户管理页
- 新增页面：`http://localhost:8088/users.html`
- 新增接口能力：
  - `GET /api/platform/users/`
  - `POST /api/platform/users/create/`
  - `GET /api/platform/users/<id>/`
  - `PATCH /api/platform/users/<id>/`
  - `POST /api/platform/users/<id>/reset-password/`
- 仅 admin 可访问

### 页面能力
- 账户列表
- 搜索与筛选
- 创建账户
- 修改角色
- 启停账户
- 重置密码

### 结果
形成平台账户管理的最小可用后台。

---

## 阶段 14：用户删除与统计增强
- 新增：`DELETE /api/platform/users/<id>/`
- 禁止删除当前登录管理员自己
- 用户管理页新增：
  - 删除按钮
  - 二次确认
  - 账户总数统计
  - admin/operator/viewer 数量统计

### 结果
用户管理页具备更完整的管理能力。

---

## 阶段 15：开发过程文档化
- 新增：`docs/agent-worklog.md`
- 新增：`docs/change-timeline.md`

### 目的
把“对话中的需求”和“代码中的结果”落为可长期保存的项目文档。

---

# 当前主要访问地址汇总

## 平台侧
- 首页：`http://localhost:8088/`
- 登录页：`http://localhost:8088/login.html`
- 用户管理页：`http://localhost:8088/users.html`
- 指挥大屏：`http://localhost:8088/bigscreen.html`
- Django API：`http://localhost:8008/api/`

## 视频侧
- WVP 登录：`http://localhost:28080/#/login`
- WVP 后台：`http://localhost:28080/`
- Knife4j：`http://localhost:28080/doc.html`
- Swagger UI：`http://localhost:28080/swagger-ui/index.html`
- ZLM：`http://localhost:28082`

---

# 近期关键提交
- `feat: add platform login and role-based menus`
- `feat: apply role-aware session menus on dashboard`
- `feat: add admin user management page`
- `feat: add user deletion and summary stats`
- `docs: add agent worklog`

---

# 建议的后续时间线节点
- 阶段 16：首页升级为正式后台布局
- 阶段 17：视频矩阵接入真实播放流
- 阶段 18：用户管理加入审计日志
- 阶段 19：静态 dist 页面迁移到正式 Vue 工程
