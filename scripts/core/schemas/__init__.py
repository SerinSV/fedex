from typing import Any, Dict, Literal, Optional

from pydantic import BaseModel, Field, root_validator


class Deployment(BaseModel):
    name: Optional[str] = Field(None, title="Deployment name")
    image: Optional[str] = Field(None, title="Container image")
    command: Optional[list] = Field(
        None, title="Command to execute inside the container"
    )
    args: Optional[list] = Field(None, title="Args to execute the container")
    environment: Optional[Dict] = Field({}, title="Environment variables")
    ports: Optional[Any] = Field(None, title="Port mappings")
    volumes: Optional[Any] = Field(None, title="Volume bindings")
    cpu_limit: Optional[float] = Field(None, title="CPU limit")
    mem_limit: Optional[str] = Field(None, title="Memory limit")
    user_name: Optional[str] = Field(None, title="Username")
    password: Optional[str] = Field(None, title="Password")
    registry_url: Optional[str] = Field(None, title="Registry Url")
    labels: Optional[dict] = Field(None, title="Labels for the deployment")
    match_labels: Optional[dict] = Field(None, title="Labels for the deployment")
    network: Optional[str] = Field(None, title="Network mode")
    runtime: Optional[str] = Field(None, title="Container runtime")
    mem_request: Optional[str] = Field(None, title="Memory resource request")
    cpu_request: Optional[float] = Field(None, title="CPU resource request")
    restart_policy: Optional[Any] = Field(None, title="Restart Policy request")


class DockerDeployment(Deployment):
    cpu_shares: Optional[int] = Field(None, title="CPU shares")
    cpu_count: Optional[int] = Field(None, title="CPU count")
    detach: Optional[bool] = Field(True, title="Detached mode")
    privileged: Optional[bool] = Field(None, title="Privileged mode")
    custom_url: Optional[str] = Field(None, title="Custom Docker Client URL")
    devices: Optional[list] = Field(None, title="Custom Docker Client URL")
    device_requests: Optional[list] = Field(None, title="Custom Docker Client URL")


    @root_validator
    def restart_policy_update(cls, values):
        if not values["restart_policy"] and values["restart_policy"] not in {
            "on-failure",
            "unless-stopped",
            "always",
            "no",
        }:
            values["restart_policy"] = {"Name": "always"}
        else:
            values["restart_policy"] = {"Name": values["restart_policy"]}
        return values


class KubernetesDeployment(Deployment):
    replicas: Optional[int] = Field(1, title="Number of pod replicas")
    namespace: Optional[str] = Field("default", title="Namespace")
    image_pull_policy: Optional[Literal["Always", "IfNotPresent", "Never"]]
    image_pull_secrets: Optional[list] = Field([], title="Image Pull Secrets")

    @root_validator
    def restart_policy_update(cls, values):
        if not values["restart_policy"] and values["restart_policy"] not in {
            "Always",
            "OnFailure",
            "Never",
        }:
            values["restart_policy"] = "Always"
        return values
