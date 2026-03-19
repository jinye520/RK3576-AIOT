# MySQL Init Scripts

此目录用于放置 MySQL 初始化脚本。

## 当前内容

- `001-wvp-init.sql`：已落地官方 WVP 2.7.4 初始化 SQL

## 使用说明

- 该脚本只会在 **MySQL 数据目录首次初始化** 时由 `mysql` 容器自动执行
- 如果当前 MySQL 数据卷已经存在，新增或修改 init SQL **不会自动重跑**
- 若要验证冷启动初始化流程，需要先清理对应 MySQL 数据卷/数据目录，再重新启动基础与视频子系统

## 建议后续补充

- `002-platform-seed.sql`：平台侧演示种子数据（可选）
