# 数据目录权限修复

当前项目在 Docker 首次运行后，以下目录可能被容器以 `root:root` 创建：

- `data/wvp`
- `data/zlm`
- `data/record`

这会导致后续宿主机侧无法直接写入或替换文件，例如：

- `data/wvp/wvp-pro.jar`
- `data/wvp/runtime-override/static/*`
- `data/zlm/www/*`
- `data/record/*`

## 自动修复脚本

项目已提供：

```bash
./scripts/fix-data-permissions.sh
```

## 脚本行为

- 检查当前目录属主
- 尝试执行：

```bash
sudo chown -R $(id -un):$(id -gn) data/wvp data/zlm data/record
```

- 成功后统一目录权限为 `755`
- 成功后统一文件权限为 `644`

## 注意

当前 agent 运行环境中的 `sudo` 需要交互式输入密码，因此脚本无法在无交互场景下替你完成提权。

如果脚本提示需要交互式密码，请在宿主机终端手动执行：

```bash
sudo chown -R $(id -un):$(id -gn) data/wvp data/zlm data/record
find data/wvp data/zlm data/record -type d -exec chmod 755 {} \;
find data/wvp data/zlm data/record -type f -exec chmod 644 {} \;
```

## 建议时机

- 第一次启动完整视频子系统后
- 替换 `wvp-pro.jar` 前
- 重新生成 `runtime-override/static` 前
- 准备迁移到 RK3576 设备前
