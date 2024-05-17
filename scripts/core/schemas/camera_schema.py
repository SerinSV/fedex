from typing import Optional

from pydantic import BaseModel

class AddCameraRequest(BaseModel):
    camera_id: Optional[str]
    mqtt_topic: Optional[str]
    docker_image: Optional[str]
    conf: Optional[str]
    url: Optional[str]

class DeleteCameraRequest(BaseModel):
    camera_id: Optional[str]


class PublishDataRequest(BaseModel):
    message: Optional[str]
    mqtt_topic: Optional[str]




