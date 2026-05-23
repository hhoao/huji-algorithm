import unittest

from src.main.utils import path_utils, video_utils
from src.test.base.test_base import TestCaseBase


class TestVideoUtils(TestCaseBase):
    def _setup_internal(self):
        pass

    def test_get_video_info(self):
        video_info = video_utils.get_video_base_info(
            path_utils.get_resource("/video/examples/test.mp4"),
        )
        print(video_info)

    @unittest.skip("Requires a local video file; set input_video before running.")
    def test_resize(self):
        input_video = path_utils.get_resource("/video/examples/test.mp4")
        video_utils.resize_video_ratio(
            input_video,
            width=520,
            output_file="test.mp4",
        )
