import logging
from typing import List, NamedTuple

import numpy as np
from aiomultiprocess import Process
from aiomultiprocess.types import Queue

from freemocap.prod.cam.detection.cam_singleton import get_or_create_cams
from jon_scratch.opencv_camera import OpenCVCamera


def create_opencv_cams():
    cams = get_or_create_cams()
    raw_webcam_obj = cams.cams_to_use
    cv_cams = [
        OpenCVCamera(port_number=webcam.port_number)
        for webcam in raw_webcam_obj
        if int(webcam.port_number) < 3
    ]
    for cv_cam in cv_cams:
        cv_cam.connect()
    return cv_cams


async def start_camera_capture(queue: Queue):
    processes = []
    creator = CameraCaptureProcess()
    process = Process(
        target=creator.run,
        args=(queue,)
    )
    process.start()
    processes.append(process)


class FramePayload(NamedTuple):
    port_number: int
    image: np.ndarray
    timestamp: int


class ImagePayload(NamedTuple):
    frames: List[FramePayload]


class CameraCaptureProcess:
    async def run(self, queue):
        cv_cams = create_opencv_cams()
        _queue = queue
        _logger = logging.getLogger(__name__)
        _logger.info("Beginning Camera Capture Process")
        while True:
            image_list: List[FramePayload] = []
            for cv_cam in cv_cams:
                success, image, timestamp = cv_cam.get_next_frame()

                if not success:
                    print(f'failed to read frame from camera at port {str(cv_cam.port_number)}')
                    continue
                if image is None:
                    print(f'Read `None` frame from camera at port {str(cv_cam.port_number)}')
                    continue
                image_list.append(
                    FramePayload(
                        port_number=cv_cam.port_number,
                        image=image,
                        timestamp=timestamp
                    )
                )

            _queue.put(
                ImagePayload(frames=image_list)
            )
