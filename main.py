import argparse
import importlib.util
import json
import os
import sys
from pathlib import Path
from typing import Any


def _venv_python() -> str | None:
    venv_dir = Path(__file__).resolve().parent / ".venv"
    if sys.platform == "win32":
        candidate = venv_dir / "Scripts" / "python.exe"
    else:
        candidate = venv_dir / "bin" / "python"
    return str(candidate) if candidate.is_file() else None


def _check_runtime_deps() -> None:
    if importlib.util.find_spec("ruamel.yaml") is None:
        print("未找到 Python 依赖，请先安装并激活虚拟环境：", file=sys.stderr)
        if sys.platform == "win32":
            print("  .\\setup.ps1", file=sys.stderr)
            print("  .venv\\Scripts\\activate", file=sys.stderr)
        else:
            print("  ./setup.sh", file=sys.stderr)
            print("  source .venv/bin/activate", file=sys.stderr)
        venv_python = _venv_python()
        if venv_python:
            print(f"  或直接: {venv_python} main.py ...", file=sys.stderr)
        sys.exit(1)


_check_runtime_deps()

from src import CONFIG_PATH
from src.main.config.config import Config, load_config
from src.main.constant.autoclip_constant import BadmintonAutoClipConfig, MatchType
from src.main.constant.common_constant import JobType
from src.main.core.badminton_auto_clipper import BadmintonAutoClipper
from src.main.core.pingpong_auto_clipper import PingPongAutoClipper
from src.main.logger import LOG
from src.main.service.large_model_service import LargeModelService
from src.main.utils import path_utils


def _build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description="乒乓球、羽毛球比赛视频自动剪辑",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python main.py --video-path videos/demo.mp4 --sport ping_pong
  python main.py --video-path videos/demo.mp4 --sport badminton --match-type doubles
  python main.py --serve
  python main.py --train
  python main.py
        """,
    )
    parser.add_argument(
        "--config",
        default=CONFIG_PATH,
        help=f"配置目录（含 application.yml），默认 {CONFIG_PATH}",
    )
    parser.add_argument("--video-path", "-v", metavar="PATH", help="本地视频文件路径")
    parser.add_argument(
        "--sport",
        choices=["ping_pong", "badminton"],
        help="运动类型（clip 模式必填）",
    )
    parser.add_argument(
        "--match-type",
        choices=["singles", "doubles"],
        default="singles",
        help="羽毛球比赛类型，默认 singles",
    )
    parser.add_argument("--output-dir", "-o", metavar="DIR", help="剪辑输出目录")
    parser.add_argument("--serve", action="store_true", help="启动 Kafka + HTTP 服务")
    parser.add_argument("--train", action="store_true", help="训练模型")
    return parser


def _resolve_mode(args: argparse.Namespace) -> str:
    modes = [bool(args.video_path), args.serve, args.train]
    if sum(modes) > 1:
        LOG.error("不能同时指定 --video-path、--serve、--train")
        sys.exit(1)
    if args.video_path:
        return "clip"
    if args.serve:
        return "serve"
    if args.train:
        return "train"
    return "config"


def _build_auto_clip_config(args: argparse.Namespace) -> dict[str, Any] | None:
    if args.sport != "badminton":
        return None
    match_type = (
        MatchType.DOUBLES_MATCH if args.match_type == "doubles" else MatchType.SINGLES_MATCH
    )
    return json.loads(BadmintonAutoClipConfig(match_type=match_type).model_dump_json())


def run_clip(args: argparse.Namespace, config: Config) -> None:
    video_path = os.path.abspath(args.video_path)
    if not os.path.isfile(video_path):
        LOG.error(f"视频文件不存在: {video_path}")
        sys.exit(1)
    if not args.sport:
        LOG.error("clip 模式需要指定 --sport（ping_pong 或 badminton）")
        sys.exit(1)

    auto_clip_config = config.auto_clip_config
    common_options = auto_clip_config.common_options
    if args.output_dir:
        common_options.output_dir = path_utils.get_project_path(args.output_dir)

    large_model_service = LargeModelService(config.large_model_service_config)
    if args.sport == "ping_pong":
        clipper = PingPongAutoClipper(
            auto_clip_config.ping_pong, common_options, large_model_service
        )
    else:
        clipper = BadmintonAutoClipper(
            auto_clip_config.badminton, common_options, large_model_service
        )

    LOG.info(f"开始剪辑: {video_path}")
    result = clipper.autoclip_video(
        video_path,
        auto_clip_config=_build_auto_clip_config(args),
    )
    LOG.info(f"剪辑完成: {result.all_match_merged_video_path}")
    print(result.all_match_merged_video_path)


def run_serve(config: Config) -> None:
    from src.main.http.internal_http import InternalHttp
    from src.main.service.video_edit_service import VideoEditService

    auto_clip_config = config.auto_clip_config
    common_options = auto_clip_config.common_options
    large_model_service = LargeModelService(config.large_model_service_config)
    http_client = InternalHttp(config.internal.http).client

    pingpong_auto_clipper = PingPongAutoClipper(
        auto_clip_config.ping_pong, common_options, large_model_service
    )
    badminton_auto_clipper = BadmintonAutoClipper(
        auto_clip_config.badminton, common_options, large_model_service
    )

    video_edit_service = VideoEditService(
        service_config=config.service_config,
        mysql_config=config.datasource_config.mysql,
        pingpong_auto_clipper=pingpong_auto_clipper,
        badminton_auto_clipper=badminton_auto_clipper,
        kafka_config=config.kafka_config,
        http_client=http_client,
    )
    try:
        video_edit_service.start()
    except Exception as e:
        video_edit_service.stop()
        LOG.error(f"启动服务失败: {e}")


def run_train(config: Config) -> None:
    large_model_service = LargeModelService(config.large_model_service_config)
    large_model_service.train()


def run_from_config(config: Config) -> None:
    if config.job_type == JobType.TRAIN_MODEL:
        run_train(config)
    elif config.job_type == JobType.SERVICE:
        run_serve(config)
    else:
        LOG.error(f"未知的 job_type: {config.job_type}")
        sys.exit(1)


def main() -> None:
    parser = _build_parser()
    args = parser.parse_args()
    config = load_config(args.config)
    mode = _resolve_mode(args)

    if mode == "clip":
        run_clip(args, config)
    elif mode == "serve":
        run_serve(config)
    elif mode == "train":
        run_train(config)
    else:
        run_from_config(config)


if __name__ == "__main__":
    main()
