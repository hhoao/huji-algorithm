import unittest

from src.main.constant.autoclip_constant import badminton_classes_mapping, ping_pong_classes_mapping
from src.main.core.badminton_action_segment_detector import BadmintonActionSegmentDetector
from src.main.core.badminton_auto_clipper import BadmintonAutoClipper
from src.main.core.ping_pong_action_segment_detector import PingPongActionSegmentDetector
from src.main.core.pingpong_auto_clipper import PingPongAutoClipper
from src.main.service.large_model_service import LargeModelService
from src.main.train.train_helper import create_classify_frames
from src.test.base.test_base import TestCaseBase


class TestTrainHelper(TestCaseBase):
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
        self.ping_pong_action_segment_detector: PingPongActionSegmentDetector = (
            PingPongActionSegmentDetector(
                is_ignore_playback=True,
                is_merge_fire_ball_and_play_ball=False,
            )
        )
        self.badminton_action_segment_detector: BadmintonActionSegmentDetector = (
            BadmintonActionSegmentDetector(
                is_ignore_playback=True,
            )
        )

    @unittest.skip("Requires local training videos; set paths before running.")
    def test_ping_pong_create_classify_frames(self):
        create_classify_frames(
            self.ping_pong_auto_clipper,
            self.ping_pong_action_segment_detector,
            "/path/to/your/training/video.mp4",
            self.config.auto_clip_config.ping_pong.singles_model,
            ping_pong_classes_mapping,
            "/path/to/your/output/ping_pong",
        )

    @unittest.skip("Requires local training videos; set paths before running.")
    def test_badminton_create_classify_frames(self):
        create_classify_frames(
            self.badminton_auto_clipper,
            self.badminton_action_segment_detector,
            "/path/to/your/training/video.mp4",
            self.config.auto_clip_config.badminton.singles_model,
            badminton_classes_mapping,
            "/path/to/your/output/badminton",
        )
