# WVP Runtime Layout

当前项目中的 `wvp` 已不再是纯占位服务，而是基于真实 WVP 运行路径工作。

## 当前目录约定

```text
data/wvp/
├── wvp-pro.jar
├── runtime-override/
│   └── static/
└── logs/
```

## 说明

- `wvp-builder` 会优先构建 `wvp-pro.jar`
- 若检测到源码目录可用，还会自动构建 Vue 前端静态资源到 `runtime-override/static/`
- `start-wvp.sh` 会在启动时优先挂载 `runtime-override/static/`，从而恢复原 WVP Vue 管理后台入口

## 当前可验证入口

- `http://localhost:28080/`
- `http://localhost:28080/#/login`
- `http://localhost:28080/doc.html`
- `http://localhost:28080/swagger-ui/index.html`
