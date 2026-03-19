# WVP 真实接入说明

当前项目已基于官方仓库结构整理出真实接入所需的关键文件与配置：

- `docker/wvp/application-docker.yml`
- `docker/zlm/config.ini`
- `docker/wvp/start-wvp.sh`
- `docker/mysql/init/001-wvp-init.sql`（已落地官方 2.7.4 初始化 SQL）

## 官方参考仓库

- https://github.com/648540858/wvp-GB28181-pro

## 当前状态

- ZLMediaKit 已接入官方风格配置
- WVP 已切换到官方风格 `application-docker.yml`
- WVP 启动脚本已支持真实 jar 启动
- `wvp-builder` 服务已加入视频 compose，可自动构建 JAR
- 已验证 WVP 2.7.4 JAR 可以启动到服务初始化阶段
- 已验证 SIP 8116 启动成功
- 已修复 ZLM secret 不一致导致的节点连接失败问题
- 已验证 WVP 登录 API 可用，媒体节点列表可返回在线节点
- Django `/api/video/status/` 已升级为主动探测，当前可返回 `wvp=running`、`zlm=running`
- 已验证 WVP 对外可访问的管理/文档入口为 `http://localhost:28080/doc.html` 与 `http://localhost:28080/swagger-ui/index.html`
- 已验证 `http://localhost:28080/v3/api-docs` 可正常返回 OpenAPI 文档
- 已修复当前运行包未发布原 Vue 静态前端的问题，现已恢复 `http://localhost:28080/` 与 `http://localhost:28080/#/login` 入口
- 已将前端恢复方案固化到 `start-wvp.sh` 运行时覆盖机制，并补充 `wvp-builder` 自动构建 runtime static 的路径
- 已完成冷启动验证：清理后重启可自动建表、生成 admin 账户，并恢复 WVP/ZLM 联通与登录能力
- 当前剩余问题集中在宿主机目录权限修复与真实设备联调
- 已补充 `scripts/fix-data-permissions.sh` 与 `docs/permissions-recovery.md` 用于宿主机侧收口处理

## 仍需人工确认的关键点

1. `data/wvp/` 目录当前权限为 root，需要在宿主机修正权限后再写入 jar
2. 首次 MySQL 初始化时需保证 `wvp` 数据库使用官方 SQL 建表
3. 如果当前 MySQL 数据目录已存在，init SQL 不会自动重跑，需要清卷后验证冷启动流程
4. SIP / RTP / Stream IP 需要根据真实部署环境微调

## 推荐下一步

1. 修复 `data/wvp` 与 `data/zlm` 宿主机目录权限
2. 结合真实摄像机/国标设备做注册、点播、回放联调
3. 视需要补充 Django 对 WVP 运行态的更细粒度主动探测
4. 验证：
   - `http://localhost:28080`
   - `http://localhost:28082`
   - `/api/video/status/`
   - WVP 管理页面
   - ZLM 节点在线状态
