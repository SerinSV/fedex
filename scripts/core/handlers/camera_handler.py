from typing import Any

from loguru import logger

from scripts.core.schemas import DockerDeployment
from scripts.core.schemas.camera_schema import AddCameraRequest, DeleteCameraRequest, PublishDataRequest
from scripts.core.utils.docker_utils import DockerManager
from scripts.core.utils.mqtt_publish import MQTTPublisher


class CameraHandler:
    def __init__(self):
        pass

    def add_camera(self, content: AddCameraRequest):
        self.add_container(content)

    def add_container(self, content: AddCameraRequest):
        env_var = dict(
            CAMERA_ID=content.camera_id
        )

        docker_config = dict(name=f"{content.camera_id}",
                             image=content.docker_image,
                             environment=env_var,
                             restart_policy="always", )

        docker_manager = DockerManager(
            DockerDeployment(
                **docker_config
            )
        )
        if docker_manager.deploy_deployment(upgrade=False):
            logger.info("Deployment Started..")
            return True
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

    def publish_data(self, data: PublishDataRequest):
        return MQTTPublisher(data.message, data.mqtt_topic).publish()
