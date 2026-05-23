import json

from src.main.constant.autoclip_constant import BadmintonAutoClipConfig, MatchType
from src.main.core.badminton_auto_clipper import BadmintonAutoClipper
from src.main.core.pingpong_auto_clipper import PingPongAutoClipper
from src.main.service.large_model_service import LargeModelService
from src.main.utils.path_utils import get_resource
from src.test.base.test_base import TestCaseBase


class TestAutoClipper(TestCaseBase):
    def _setup_internal(self):
        large_model_service = LargeModelService(self.config.large_model_service_config)
        self.ping_pong_auto_clipper: PingPongAutoClipper = PingPongAutoClipper(
            self.config.auto_clip_config.ping_pong,
            self.config.auto_clip_config.common_options,
            large_model_service,
        )
        self.badminton_auto_clipper: BadmintonAutoClipper = BadmintonAutoClipper(
            self.config.auto_clip_config.badminton,
            self.config.auto_clip_config.common_options,
            large_model_service,
        )

    def test_ping_pong_clip(self):
        self.ping_pong_auto_clipper.autoclip_video(get_resource("video/examples/test.mp4"))

    def test_badminton_clip(self):
        self.badminton_auto_clipper.autoclip_video(get_resource("video/examples/blue.mp4"))

    def test_badminton_double_clip(self):
        config = BadmintonAutoClipConfig(match_type=MatchType.DOUBLES_MATCH)
        self.badminton_auto_clipper.autoclip_video(
            input_video_path=get_resource("video/examples/badminton_doubles_1.mp4"),
            auto_clip_config=json.loads(config.model_dump_json()),
        )

    # def test_predict(self):
    #     model = YOLO(model_path)
    #     results =model(frames, stream=True, stream_buffer=True)
    #     # res = model.predict(frames, stream=True)  # type: ignore
    #     for result in results:
    #         top1: str = result.names[r.probs.top1]  # type: ignore
    #         ret.append(top1)
