# Docker

## 开发环境（Kafka）

本地消息队列，无需密钥：

```bash
cd docker/dev
docker compose up -d
```

Kafka 对外端口：`localhost:9094`（与 `application.yml` 中 `kafka.bootstrap_servers` 一致）。

## 构建算法镜像

```bash
# 可选：配置私有仓库（不配置则只本地 build，不 push）
cp docker/build.env.example docker/build.env
# 编辑 docker/build.env

./docker/autoclip-algorithm/build.sh
```

构建流程：

1. `git archive` 打包当前分支代码（含默认 `application*.yml`，密钥为占位符）
2. 在 `docker/autoclip-algorithm/internal/` 下 `docker build`
3. 若设置了 `DOCKER_REGISTRY`，则 tag 并 push

## 运行生产镜像

镜像内自带默认配置。生产环境请挂载真实配置或设置环境变量覆盖 COS、API 令牌等：

```bash
docker run --gpus all \
  -v /path/to/application_prod.yml:/autoclip/algorithm/src/resources/application_prod.yml:ro \
  -e env=prod \
  autoclip-algorithm:latest
```

## Ray 镜像

```bash
./docker/ray/build.sh
```

若构建时需要代理，在 `docker/build.env` 中设置 `HTTP_PROXY` / `HTTPS_PROXY`。
