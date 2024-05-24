import json
from datetime import datetime
from typing import Any

from loguru import logger
from docker import types

from scripts.configurations import volume
from scripts.core.schemas import DockerDeployment
from scripts.core.schemas.camera_schema import AddCameraRequest, DeleteCameraRequest, PublishDataRequest
from scripts.core.utils.docker_utils import DockerManager
from scripts.core.utils.common_utils import CommonUtils
from scripts.core.utils.mqtt_publish import MQTTPublisher


class CameraHandler:
    def __init__(self):
        pass

    def add_camera(self, content: AddCameraRequest):

        # the camera details need to be stored in a database and fetched from the db instead of reading from a json in the
        # next phase.

        with open("camera_details.json") as outfile:
            camera_details = json.load(outfile)
        if content.camera_id in camera_details:
            mask_details = json.dumps(camera_details[content.camera_id])
        else:
            mask_details = None
        return self.add_container(content, mask_details)

    def add_container(self, content: AddCameraRequest, mask_details):

        container_name = CommonUtils.generate_id(f"{content.camera_id}")
        env_var = dict(
            camera_id=content.camera_id,
            video_source=content.url,
            mask_details=mask_details,
            conf=content.conf,
            mqtt_topic=content.mqtt_topic
        )
        devices = [types.DeviceRequest(driver="nvidia", device_ids=["all"], capabilities=[["gpu"]])]
        volumes = [volume.volume]
        docker_config = dict(name=container_name,
                             image=content.docker_image,
                             environment=env_var,
                             restart_policy="always",
                             volumes=volumes,
                             device_requests=devices)

        docker_manager = DockerManager(
            DockerDeployment(
                **docker_config
            )
        )
        if docker_manager.deploy_deployment(upgrade=False):
            logger.info(f"Deployment Started with container name {container_name}")
            return container_name
        return False

    def delete_camera(self, camera: DeleteCameraRequest):
        self.remove_container(camera=camera)

    def remove_container(self, camera: DeleteCameraRequest) -> Any:
        container_name = camera.camera_id
        docker_deployment_details = DockerDeployment(
            name=container_name)
        docker_manager = DockerManager(docker_deployment_details)
        if docker_manager.delete_deployment():
            logger.info(
                "Removing camera container -> {}".format(camera.camera_id)
            )
            return True
        return False

    def transform_data(self, input_data):
        data = json.loads(input_data['message'])

        records = [
            {"TagName": "section_1", "Value": data["fill_volume_perc"]["section_1"]},
            {"TagName": "section_2", "Value": data["fill_volume_perc"]["section_2"]},
            {"TagName": "section_3", "Value": data["fill_volume_perc"]["section_3"]},
            {"TagName": "section_4", "Value": data["fill_volume_perc"]["section_4"]},
            {"TagName": "Total Area", "Value": data["fill_volume_perc"]["Total Area"]},
            {"TagName": "camera_id", "Value": data["camera_id"]}
        ]

        timestamp = datetime.strptime(data["timestamp"], "%d/%m/%Y %H:%M:%S")

        return {
            "records": records,
            "Timestamp": timestamp.isoformat(timespec='milliseconds') + "+00:00"
        }

    def publish_data(self, data: PublishDataRequest):
        transformed_data = self.transform_data(data.dict())
        logger.info(f"transformed_data {transformed_data}")
        logger.debug(f"Publishing data to MQTT topic: {data.mqtt_topic}")
        return MQTTPublisher(json.dumps(transformed_data), data.mqtt_topic).publish()
