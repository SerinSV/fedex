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
        camera_details = {"ps5": {
            "total_area_point": [[249, 419], [336, 318], [343, 296], [378, 371], [547, 365], [555, 325], [563, 325],
                                 [598, 364], [703, 356], [703, 300], [528, 177], [405, 97], [342, 61], [324, 48],
                                 [280, 23], [228, 12], [226, 76], [229, 174], [237, 312], [247, 420]],
            "section": [(320, 480), (184, 320), (68, 184), (0, 68)]},
            "pf13": {"total_area_point": [[525, 0], [550, 0], [550, 480], [0, 480], [0, 320]],
                     "section": [(240, 480), (100, 240), (30, 100), (0, 30)]},
            "ps15": {
                "total_area_point": [[1, 346], [458, 356], [749, 345], [891, 328], [937, 314], [892, 282],
                                     [763, 209], [650, 148], [549, 90], [483, 61], [469, 58], [447, 55],
                                     [417, 65], [366, 88], [257, 140], [104, 220], [2, 274]],
                "section": [(320, 480), (200, 320), (96, 200), (0, 96)]}}
        if content.camera_id in camera_details:
            mask_details = camera_details[content.camera_id]
        else:
            mask_details = ""
        self.add_container(content, mask_details)

    def add_container(self, content: AddCameraRequest, mask_details):

        env_var = dict(
            CAMERA_ID=content.camera_id,
            MASK_DETAILS=mask_details
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
