# Huji Algorithm

Auto-clip table tennis and badminton match videos: detect rally segments, filter ball pickup/replay, output highlights.

[中文](README.md)

## Features

- Pass in a video file; auto-detect and clip match play
- Table tennis and badminton (singles / doubles)
- Local files and remote object storage (COS/OSS)

## Prerequisites

- Python 3.12+
- [FFmpeg](https://ffmpeg.org/) on `PATH` (used when merging clipped segments)
- GPU optional; on Windows if PyTorch install fails, pick the right CUDA build from [pytorch.org](https://pytorch.org) and `pip install`

## Quick start

### Local quick clip (recommended)

**Linux / macOS**

```bash
./setup.sh
source .venv/bin/activate

python main.py --video-path videos/demo.mp4 --sport ping_pong
python main.py -v src/resources/video/examples/test.mp4 --sport badminton --match-type doubles
```

**Windows (PowerShell)**

```powershell
.\setup.ps1
.venv\Scripts\activate

python main.py --video-path videos\demo.mp4 --sport ping_pong
python main.py -v src\resources\video\examples\test.mp4 --sport badminton --match-type doubles
```

If `setup.ps1` is blocked by execution policy, install manually:

```powershell
python -m venv .venv
.venv\Scripts\pip install -r requirements.txt
.venv\Scripts\python main.py --video-path videos\demo.mp4 --sport ping_pong
```

### Service mode (Kafka + HTTP)

```bash
cd docker/dev && docker compose up -d
python main.py --serve
```

On Windows, install [Docker Desktop](https://www.docker.com/products/docker-desktop/).

### CLI flags

| Flag | Description |
| ---- | ----------- |
| `--video-path` / `-v` | Local video file path |
| `--sport` | `ping_pong` or `badminton` (required for clip mode) |
| `--match-type` | Badminton: `singles` (default) / `doubles` |
| `--output-dir` / `-o` | Clip output dir (overrides `output_dir` in config) |
| `--config` | Config directory, default `src/resources` |
| `--serve` | Start Kafka + HTTP service |
| `--train` | Train models |

When clipping finishes, the merged video path is printed to the terminal; default output is `output/clipped/` (override with `-o`).

Sample videos: `src/resources/video/examples/`.

`src/resources/application*.yml` ships with runnable defaults (local Kafka, sample model paths).  
For remote COS or backend API integration, update placeholders:

| Config key | Description |
| ---------- | ----------- |
| `filesystem.cos.*` | Object storage keys & bucket |
| `internal.http.access_token` | Backend API token |
| `datasource.mysql.*` | MySQL (remote file config lookup) |

Environment variables can override config (dots → underscores); see `.env.example`. Jasypt supported: `ENC(ciphertext)` + `JASYPT_PASSWORD`.

## Development

### Install dependencies

Linux / macOS: `./setup.sh`  
Windows: `.\setup.ps1`

### Configuration

- `application.yml` — shared config
- `application_dev.yml` — loaded when `env: dev`
- `application_prod.yml` — loaded when `env: prod`

### Tests

```bash
python -m unittest discover -s src/test -p "test_*.py"
```

## Community

- **QQ Group**: 112856301
- **Discord**: [Join our server](https://discord.com/channels/1518551459053178960/1518551461242474558)
