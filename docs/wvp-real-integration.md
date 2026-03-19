# WVP 真实接入说明

当前项目已基于官方仓库结构整理出真实接入所需的关键文件与配置：

- `docker/wvp/application-docker.yml`
- `docker/zlm/config.ini`
- `docker/wvp/start-wvp.sh`
- `docker/mysql/init/001-wvp-init.sql`（当前为占位，需要替换为官方 SQL）

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
- 当前剩余问题集中在数据库初始化固化与前端静态资源/管理页面收口

## 仍需人工确认的关键点

1. 初始化 SQL 需要使用官方版本对应的真实内容替换当前占位文件
2. `data/wvp/` 目录当前权限为 root，需要在宿主机修正权限后再写入 jar
3. 首次 MySQL 初始化时需保证 `wvp` 数据库使用官方 SQL 建表
4. SIP / RTP / Stream IP 需要根据真实部署环境微调

## 推荐下一步

1. 修复 `data/wvp` 与 `data/zlm` 宿主机目录权限
2. 将官方 2.7.4 MySQL 初始化脚本正式落地到 `docker/mysql/init/001-wvp-init.sql`
3. 清空并重建 MySQL 数据卷后重新启动视频栈
4. 验证 WVP 管理页面、默认登录流程与节点状态展示
5. 视需要补充 Django 对 WVP 运行态的主动探测
6. 验证：
   - `http://localhost:28080`
   - `http://localhost:28082`
   - `/api/video/status/`
   - WVP 管理页面
   - ZLM 节点在线状态
