import docker
import urllib3
from docker.errors import APIError, DockerException, NotFound
from loguru import logger

from scripts.core.exceptions.exception_codes import (
    DockerExceptionCode as docker_exception,
)
from scripts.core.exceptions.module_exceptions import DockerUnknownConnectionType
from scripts.core.schemas import DockerDeployment
from scripts.core.utils.common_utils import CommonUtils


class DockerUtility(CommonUtils):
    def __init__(self):
        super().__init__()

    def docker_url(self):
        if self.docker_connect_mode() == self.docker_socket_mode():
            url = "unix:/{path}".format(path=self.docker_socket_path())
        elif self.docker_connect_mode() == self.docker_tcp_mode():
            url = "tcp://{host}:{port}".format(
                host=self.docker_api_host(), port=self.docker_api_port()
            )
        else:
            raise DockerUnknownConnectionType(
                docker_exception.DAEX106.format(conn=self.docker_socket_mode())
            )
        return url

    def docker_client(self, url: str = None):
        try:
            if url:
                client = docker.DockerClient(base_url=url)
            else:
                client = docker.DockerClient(base_url=self.docker_url())
        except urllib3.connectionpool.MaxRetryError:
            logger.warning(docker_exception.DAEX107)
            client = None
        except urllib3.connectionpool.HTTPConnection:
            logger.warning(docker_exception.DAEX107)
            client = None
        except Exception as e:
            logger.warning(f"{docker_exception.DAEX107}: {str(e)}")
            client = None
        return client


class DockerManager(DockerUtility):
    def __init__(self, deployment_details: DockerDeployment):
        super().__init__()
        self.deployment_details = deployment_details
        self.client = self.docker_client(
            deployment_details.custom_url if deployment_details.custom_url else None
        )
        if all(
            [
                self.deployment_details.user_name,
                self.deployment_details.password,
                self.deployment_details.registry_url,
            ]
        ):
            self.authenticate_with_registry(
                username=self.deployment_details.user_name,
                password=self.deployment_details.password,
                registry=self.deployment_details.registry_url,
            )

    def authenticate_with_registry(self, username, password, registry):
        try:
            self.client.login(username=username, password=password, registry=registry)
            return True
        except Exception as e:
            logger.error(
                f"Agent was unable to perform registry authentication: {e}"
            )
            return False

    @staticmethod
    def container_restart_policy():
        return {"Name": "always"}

    @staticmethod
    def container_detach_policy():
        return True

    def container_network_mode(self):
        return self.container_deploy_network_mode()

    @staticmethod
    def container_publish_ports(publish_ports):
        container_publish_ports = {}
        try:
            for ports in publish_ports:
                if not ports.get("host_port") and ports.get("container_port"):
                    continue
                if not ports.get("host_port", "").endswith("/tcp"):
                    ports["host_port"] = f"{ports['host_port']}/tcp"
                container_publish_ports[ports["host_port"]] = int(
                    ports["container_port"]
                )
            logger.debug(f"Container publish ports: {container_publish_ports}")
        except Exception as e:
            logger.debug(f"Exception Occurred in container publish ports {e}")
        return container_publish_ports

    def deploy_deployment(self, upgrade=False):
        try:
            if upgrade:
                self.stop_deployment()
                self.delete_deployment()
            docker_kwargs = dict(
                restart_policy=self.deployment_details.restart_policy,
                environment=self.deployment_details.environment,
                name=self.deployment_details.name,
                detach=self.deployment_details.detach,
                privileged=self.deployment_details.privileged,
                labels=self.deployment_details.labels,
                command=self.deployment_details.command,
                volumes=self.deployment_details.volumes,
                ports=self.container_publish_ports(
                    publish_ports=self.deployment_details.ports or {}
                ),
            )
            if self.deployment_details.devices is not None:
                docker_kwargs |= dict(devices=self.deployment_details.devices)
            if self.deployment_details.network is None:
                docker_kwargs |= dict(network_mode=self.container_network_mode())
            else:
                docker_kwargs |= dict(network=self.deployment_details.network)
            if self.deployment_details.runtime:
                docker_kwargs |= dict(runtime=self.deployment_details.runtime)
            if self.deployment_details.mem_limit is not None:
                docker_kwargs |= dict(mem_limit=self.deployment_details.mem_limit)
            if self.deployment_details.mem_request:
                docker_kwargs |= dict(
                    mem_reservation=self.deployment_details.mem_request
                )
            if self.deployment_details.cpu_request:
                docker_kwargs |= dict(
                    cpu_quota=int(self.deployment_details.cpu_request * 1e5)
                )
            if self.deployment_details.cpu_limit:
                docker_kwargs |= dict(
                    cpu_quota=int(self.deployment_details.cpu_limit * 1e5)
                )

            container = self.client.containers.run(
                image=self.deployment_details.image, **docker_kwargs
            )
            logger.debug(
                f"Container '{self.deployment_details.name}'"
                f" launched with container ID '{container.short_id}'"
            )
            return container
        except APIError as e:
            if "Conflict" in str(e):
                print(
                    f"Container with name "
                    f"'{self.deployment_details.name}' already exists."
                )
            else:
                logger.error(
                    f"Error occurred while launching the container : {str(e)}")
            raise DockerException from e
        except Exception as e:
            logger.error(
                f"Error occurred while launching the container : {str(e)}")
            raise DockerException from e

    def delete_deployment(self):
        try:
            logger.debug(f"Removing the container: {self.deployment_details.name}")
            container = self.client.containers.get(self.deployment_details.name)
            container.remove(force=True)
            return container
        except NotFound as e:
            logger.warning(f"Container {self.deployment_details.name} not found.")
            raise DockerException from e
        except Exception as e:
            logger.warning(
                f"Agent faced a problem when deleting the container: {str(e)}"
            )
            raise DockerException from e

    def stop_deployment(self):
        try:
            logger.debug(f"Stopping the container: {self.deployment_details.name}")
            container = self.client.containers.get(self.deployment_details.name)
            container.stop()
            return container
        except NotFound as e:
            logger.warning(f"Container {self.deployment_details.name} not found.")
            raise DockerException from e
        except Exception as e:
            logger.warning(
                f"Agent faced a problem when stopping the container: {str(e)}"
            )
            raise DockerException from e

    def start_deployment(self):
        try:
            logger.debug(f"Starting the container: {self.deployment_details.name}")
            container = self.client.containers.get(self.deployment_details.name)
            container.start()
            return container
        except NotFound as e:
            logger.warning(f"Container {self.deployment_details.name} not found.")
            raise DockerException from e
        except Exception as e:
            logger.warning(
                f"Agent faced a problem when starting the container: {str(e)}"
            )
            raise DockerException from e

    def restart_deployment(self):
        try:
            logger.debug(f"Restarting the container: {self.deployment_details.name}")
            container = self.client.containers.get(self.deployment_details.name)
            container.restart()
            return container
        except NotFound as e:
            logger.warning(f"Container {self.deployment_details.name} not found.")
            raise DockerException from e
        except Exception as e:
            logger.warning(
                f"Agent faced a problem when restarting the container: {str(e)}"
            )
            raise DockerException from e

    def list_containers_by_filters(self, filters):
        logger.debug(f"Listing containers with filters: {filters}")
        try:
            containers = self.client.containers.list(filters=filters)
            return containers
        except Exception as e:
            logger.warning(f"Agent faced a problem while listing containers: {str(e)}")
            return []
