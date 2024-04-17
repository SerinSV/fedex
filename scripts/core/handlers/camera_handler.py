import json
from copy import deepcopy
from typing import Any

from loguru import logger

from scripts.core.schemas import DockerDeployment
from scripts.core.schemas.camera_schema import AddCameraRequest, DeleteCameraRequest
from scripts.core.utils.common_utils import CommonUtils
from scripts.core.utils.docker_utils import DockerManager


class CameraHandler:
    def __init__(self):
        pass

    # def get_camera(
    #         self, camera_id: str = None, app_type: str = None, app_id: str = None
    # ):
    #     query = {"decommissioned": False}
    #     if app_id:
    #         query |= {"app_id": app_id}
    #     if app_type == "appsmith":
    #         if camera_id is not None:
    #             query |= {"cameraId": camera_id}
    #             camera_details = self.camera_config.find_one_camera(query=query)
    #         else:
    #             camera_details = self.camera_config.find_cameras(query=query)
    #         return camera_details
    #     else:
    #         if camera_id is not None:
    #             query |= {"cameraId": camera_id}
    #             camera_details = self.camera_config_old.find_one_camera(query=query)
    #         else:
    #             camera_details = self.camera_config_old.find_cameras(query=query)
    #
    #         return self.format_camera(camera_details)
    #
    #
    #
    # def delete_camera(self, camera: DeleteCameraRequest):
    #     self.camera_config_old.update_one_camera(
    #         query={"cameraId": camera.camera_id},
    #         data=dict(
    #             decommissioned=True,
    #         ),
    #     )
    #     self.camera_config.update_one_camera(
    #         query=camera.dict(),
    #         data=dict(
    #             decommissioned=True,
    #         ),
    #     )
    #     self.remove_container(camera=camera)
    #
    # def remove_container(self, camera: DeleteCameraRequest) -> Any:
    #     camera_meta = self.camera_config.find_one_camera(query=camera.dict())
    #     camera_name_trimmed = camera_meta.get("camera_name").replace(" ", "")
    #     container_name = camera_name_trimmed + "__" + camera.camera_id
    #     docker_deployment_details = DockerDeployment(
    #         name=container_name, custom_url=camera_meta.get("docker_client_url")
    #     )
    #     docker_manager = DockerManager(docker_deployment_details)
    #     if docker_manager.delete_deployment():
    #         logger.info(
    #             "Removing camera container -> {}".format(camera_meta.get("camera_name"))
    #         )
    #         return True
    #     return False

    def add_camera(self, content: AddCameraRequest):
        """
        Definition for adding apps
        :param content:
        :param meta_info:
        :return:
        """

        # camera_details = BaseCamera(
        #     **content.dict(),
        #     webrtc_id=webrtc_id,
        #     camera_status="Running",
        #     project_id=meta_info.project_id,
        # )

        camera_id = content.camera_id
        mount_vol = None
        source_type = None
        # if content.camera_url.startswith("rtsp"):
        #     source_type = "rtsp"
        # if content.camera_url.endswith((".avi", ".mp4")):
        #     source_type = "videofile"
        # if source_type is None:
        #     mount_vol = content.camera_url

        self.add_container(content)

    def add_container(self, content: AddCameraRequest):
        env_var = dict(
            # DEVICE_ID=camera_id,
            # RTSP_URI=camera.camera_url,
            # APP_NAME=app_data.get("app_name"),
            # PROJECT_ID=camera.project_id,
            # LOGIN_TOKEN=login_token,
            # X1=extra_field.get("x1"),
            # X2=extra_field.get("x2"),
            # Y1=extra_field.get("y1"),
            # Y2=extra_field.get("y2"),
            # ALIGNMENT=extra_field.get("alignment"),
            # PROCESSING_UNIT="gpu",  # GPU/CPU
            # IOU=0.3,
            # CONFIDENCE=0.7,
            # AGNOSTIC_NMS=True,
            # FRAME_HEIGHT=camera.camera_height,
            # FRAME_WIDTH=camera.camera_width,
            # TZ=self.time_zone.default_timezone,
            # EVENT_HOST_URI=app_data.get("app_url"),
            CAMERA_ID=content.camera_id,
            # CAMERA_NAME=camera.camera_name,
            # APP=app_data.get("app_name"),
            # HIERARCHY=camera.asset_hierarchy,
            # RTPDETAILS=json.dumps(rtp_details),
            # GET_JANUS_DETAILS="http://192.168.0.220:8554/custom/get_janus?deploymentId=",
            # DEPLOYMENT_ID="Camera124_3feda3c2",
            # LOCAL_EVENTS_PATH="events/events.txt",
        )

        docker_config = dict(name=f"{content.camera_id}",
                             image=content.docker_image,
                             environment=env_var,
                             restart_policy="always", )
        # if not camera.camera_url.startswith("rtsp://"):
        #     docker_config.update(dict(devices=['/dev/video0:/dev/video0']))
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
        return self.remove_container(camera=camera)

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
