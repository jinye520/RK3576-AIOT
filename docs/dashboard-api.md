# Dashboard 聚合接口设计

建议使用聚合接口：

- `/api/home/dashboard/`

用于一次性返回首页所需大部分数据，减少前端多次请求。

## 当前已实现内容

- 统计信息
- 视频状态
- 视频运行态（WVP 登录、admin 账户、媒体节点在线数、前端与文档可访问性）
- 端口信息
- 最新遥测
- 网关汇总
- 设备汇总
- 遥测汇总

## 相关接口

- `/api/video/status/`
- `/api/video/runtime/`
- `/api/system/status/`
- `/api/home/dashboard/`
