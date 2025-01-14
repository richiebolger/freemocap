from dataclasses import dataclass

import numpy as np



@dataclass
class LensDistortionCalibrationData:
    image_width: int
    image_height: int
    reprojection_error: float = 1e9
    camera_matrix: np.ndarray = None
    number_of_lens_distortion_coefficients: int = 4
    lens_distortion_coefficients: np.ndarray = None
    rotation_vectors_of_the_board: np.ndarray = None
    translation_vectors_of_the_board: np.ndarray = None
    lens_distortion_std_dev: float = None
    camera_location_std_dev: float = None

    def __post_init__(self):
        if self.camera_matrix is None:
            self.camera_matrix = np.array([[float(self.image_width), 0., self.image_width / 2.],
                                           [0., float(self.image_width), self.image_height / 2.],
                                           [0., 0., 1.]])

        if self.lens_distortion_coefficients is None:
            self.lens_distortion_coefficients = np.zeros((self.number_of_lens_distortion_coefficients, 1))

@dataclass
class CameraCalibrationData:
    image_width: int
    image_height: int
    lens_distortion_calibration_data: LensDistortionCalibrationData = None
    camera_translation_relative_to_camera0: np.ndarray = np.zeros((3, 1))
    camera_rotation_relative_to_camera0: np.ndarray = np.zeros((3, 1))

    def __init__(self, image_width, image_height):
        self.image_width = image_width
        self.image_height = image_height
        self.lens_distortion_calibration_data = LensDistortionCalibrationData(self.image_width,
                                                                              self.image_height)

