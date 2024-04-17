from fastapi import APIRouter, Depends

from . import camera_services

router = APIRouter()


@router.on_event("startup")
def start_app():
    print("Starting...........")


@router.on_event("shutdown")
def exit_app():
    print("Exiting...........")


router.include_router(camera_services.router)
