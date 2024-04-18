import logging

from fastapi import APIRouter

from scripts.constants.endpoints import Endpoints
from scripts.core.handlers import camera_handler_obj
from scripts.core.schemas.camera_schema import AddCameraRequest, DeleteCameraRequest, PublishDataRequest
from scripts.core.schemas.response_models import DefaultResponse, DefaultFailureResponse


router = APIRouter(prefix=Endpoints.camera_base_url, tags=["v1 | Camera"])


@router.post(Endpoints.base_url)
def add_camera(
        request_data: AddCameraRequest
):
    try:
        response = camera_handler_obj.add_camera(request_data)
        return DefaultResponse(message="Camera Added Successfully", data=response)
    except Exception as e:
        logging.exception(e)
        return DefaultFailureResponse(error="Unknown Error occurred")


@router.delete(Endpoints.base_url)
def delete_camera(
        request: DeleteCameraRequest
):
    try:
        response = camera_handler_obj.delete_camera(request)
        return DefaultResponse(
            message="Template Deleted Successfully", data=response
        )
    except Exception as e:
        logging.exception(e)
        return DefaultFailureResponse(error="Unknown Error occurred")


@router.post(Endpoints.publish_url)
def publish_data(
        request: PublishDataRequest
):
    try:
        response = camera_handler_obj.publish_data(request)
        return DefaultResponse(
            message="Data Pushed Successfully", data=response
        )
    except Exception as e:
        logging.exception(e)
        return DefaultFailureResponse(error="Unknown Error occurred")
