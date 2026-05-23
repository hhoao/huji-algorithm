# Autoclip

乒乓球、羽毛球比赛视频自动剪辑：检测比赛片段，过滤捡球/回放，输出精彩片段。

## 功能

- 传入视频文件，自动检测并剪辑比赛过程
- 支持乒乓球、羽毛球（单打/双打）
- 支持本地文件与对象存储（COS/OSS）远程处理（Kafka 消息模式）

## 快速开始

```bash
./setup.sh
cd docker/dev && docker compose up -d   # 消息模式需要 Kafka
python main.py                          # 默认读取 src/resources/application.yml
```

仓库内 `src/resources/application*.yml` 已包含可运行的默认配置（本地 Kafka、示例模型路径）。  
使用远程 COS 或对接后台 API 时，只需修改其中的占位项：

| 配置项 | 说明 |
|--------|------|
| `filesystem.cos.*` | 对象存储密钥与 bucket |
| `internal.http.access_token` | 后台 API 令牌 |
| `datasource.mysql.*` | MySQL（远程文件配置查询） |

也可用环境变量覆盖（点号改为下划线），见 `.env.example`。支持 Jasypt：`ENC(密文)` + `JASYPT_PASSWORD`。

## 如何开发

### 安装依赖

```bash
./setup.sh
```

### 环境配置

- `application.yml`：公共配置
- `application_dev.yml`：`env: dev` 时加载
- `application_prod.yml`：`env: prod` 时加载

### Kafka（消息模式）

```bash
cd docker/dev
docker compose up -d
```

生产镜像见 [docker/README.md](docker/README.md)。

### 测试

```bash
python -m unittest discover -s src/test -p "test_*.py"
```

示例视频：`src/resources/video/examples/`。
