import unittest

import torch
from ultralytics import YOLO
from ultralytics.engine.results import Results

from src.main.service.large_model_service import LargeModelService
from src.test.base.test_base import TestCaseBase


class TestFileSystemService(TestCaseBase):
    def _setup_internal(self):
        self.service = LargeModelService(self.config.large_model_service_config)

    @unittest.skip("Requires a local dataset image; set image_path before running.")
    def test_pose_predit(self):
        model = YOLO("../../resources/models/yolo/yolo11n-pose.pt")
        image_path = "/path/to/your/dataset/sample.png"

        results: list[Results] = model(  # pyright: ignore [reportUnknownVariableType]
            image_path
        )  # type: ignore

        # Access the results
        for result in results:
            result.show()  # type: ignore
            xy: torch.Tensor = result.keypoints.xy  # type: ignore
            xyn: torch.Tensor = result.keypoints.xyn  # type: ignore
            kpts: torch.Tensor = result.keypoints.data  # type: ignore
            print(xy.shape)  # type: ignore
            print(xyn.shape)  # type: ignore
            print(kpts.shape)  # type: ignore
