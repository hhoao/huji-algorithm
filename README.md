# Huji Algorithm

乒乓球、羽毛球比赛视频自动剪辑：检测比赛片段，过滤捡球/回放，输出精彩片段。

[English](README.en.md)

## 功能

- 传入视频文件，自动检测并剪辑比赛过程
- 支持乒乓球、羽毛球（单打/双打）
- 支持本地文件与对象存储（COS/OSS）远程处理

## 前置依赖

- Python 3.12+
- [FFmpeg](https://ffmpeg.org/)（需在 PATH 中，剪辑合并视频时使用）
- GPU 可选；Windows 上 PyTorch 若安装失败，请按 [pytorch.org](https://pytorch.org) 选择对应 CUDA 版本后 `pip install`

## 快速开始

### 本地快速剪辑（推荐）

**Linux / macOS**

```bash
./setup.sh
source .venv/bin/activate

python main.py --video-path videos/demo.mp4 --sport ping_pong
python main.py -v src/resources/video/examples/test.mp4 --sport badminton --match-type doubles
```

**Windows（PowerShell）**

```powershell
.\setup.ps1
.venv\Scripts\activate

python main.py --video-path videos\demo.mp4 --sport ping_pong
python main.py -v src\resources\video\examples\test.mp4 --sport badminton --match-type doubles
```

若无法执行 `setup.ps1`（执行策略限制），可手动安装：

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py --video-path videos\demo.mp4 --sport ping_pong
```

### 服务模式（Kafka + HTTP）

```bash
cd docker/dev && docker compose up -d
python main.py --serve
```

Windows 上需安装 [Docker Desktop](https://www.docker.com/products/docker-desktop/)。

### CLI 参数

| 参数 | 说明 |
|------|------|
| `--video-path` / `-v` | 本地视频文件路径 |
| `--sport` | 运动类型：`ping_pong` 或 `badminton`（clip 模式必填） |
| `--match-type` | 羽毛球比赛类型：`singles`（默认）/ `doubles` |
| `--output-dir` / `-o` | 剪辑输出目录（覆盖配置文件中的 `output_dir`） |
| `--config` | 配置目录，默认 `src/resources` |
| `--serve` | 启动 Kafka（需要配置 Kafka 服务） + HTTP 服务 |
| `--train` | 训练模型 |

剪辑完成后，终端会打印合并视频的输出路径；默认写入配置中的 `output/clipped/`（可用 `-o` 覆盖）。

示例视频：`src/resources/video/examples/`。

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

Linux / macOS：`./setup.sh`  
Windows：`.\setup.ps1`

### 环境配置

- `application.yml`：公共配置
- `application_dev.yml`：`env: dev` 时加载
- `application_prod.yml`：`env: prod` 时加载

### 测试

```bash
python -m unittest discover -s src/test -p "test_*.py"
```

## 社区

- **QQ 群**：112856301
- **Discord**：[加入群组](https://discord.com/channels/1518551459053178960/1518551461242474558)
