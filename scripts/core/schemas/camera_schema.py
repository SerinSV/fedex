import datetime
from typing import Optional, Any

from pydantic import BaseModel

from scripts.core.utils.common_utils import CommonUtils


class AddCameraRequest(BaseModel):
    camera_id: Optional[str]
    mqtt_topic: Optional[str]
    docker_image: Optional[str]
    disable: Optional[bool] = False


class DeleteCameraRequest(BaseModel):
    camera_id: Optional[str]


class PublishDataRequest(BaseModel):
    message: Optional[str]
    mqtt_topic: Optional[str]


# class DockerDetails(BaseModel):
#     mount_vol: Optional[str] = None
