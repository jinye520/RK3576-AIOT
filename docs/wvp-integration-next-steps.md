# WVP 集成下一步计划

当前项目已完成视频子系统骨架，但 WVP 仍为占位模式。

## 下一步建议

1. 下载或构建与你选择版本匹配的 WVP 可运行 JAR
2. 放置到：

```text
data/wvp/wvp-pro.jar
```

3. 准备 WVP 官方数据库初始化 SQL
4. 将 SQL 放入：

```text
docker/mysql/init/
```

5. 根据真实网络环境调整以下参数：

- SIP 域 ID
- SIP Server ID
- SIP 密码
- ZLM IP / Hook IP / Stream IP
- RTP 端口范围

6. 在 RK3576 真机环境下重点联调：

- GB28181 注册
- 实时点播
- 回放
- 录像
- NAT / 局域网 IP 问题

## 当前占位模式说明

当前 `wvp` 容器会执行 `docker/wvp/start-wvp.sh`：

- 如果检测不到 `data/wvp/wvp-pro.jar`
- 容器会进入占位模式并保持运行

这样可以确保 compose 结构先稳定存在，便于逐步接入真实包。
