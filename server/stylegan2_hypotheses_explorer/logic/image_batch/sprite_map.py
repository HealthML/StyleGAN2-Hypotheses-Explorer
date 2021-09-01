from functools import cached_property
from io import BytesIO
from pathlib import Path
from typing import List

from flask import send_file
from torch import Tensor
from torchvision.utils import save_image


class SpriteMap:
    def __init__(self, images: List[Tensor]):
        self._images = images

    @cached_property
    def _image_array(self) -> BytesIO:
        image_array = BytesIO()
        save_image(
            tensor=self._images,
            fp=image_array,
            nrow=len(self._images),
            padding=0,
            format="jpeg"
        )
        return image_array

    def send(self):
        self._image_array.seek(0)
        return send_file(self._image_array, "image/jpeg")

    def export_images(self, paths: List[Path]):
        for image, path in zip(self._images, paths):
            save_image(
                tensor=image,
                fp=path,
                format="jpeg"
            )
