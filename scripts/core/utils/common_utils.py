import platform
import random
import threading
import time
from uuid import uuid1

from scripts.configurations import container_engine


def background(f):
    """
     a threading decorator
    use @background above the function you want to run in the background
    :param f:
    :return:
    """

    def bg_f(*a, **kw):
        thread = threading.Thread(target=f, args=a, kwargs=kw)
        thread.start()

    return bg_f


class CommonUtils:
    def __init__(self, **kwargs):
        """Will be added for later purpose"""
        pass

    def docker_connect_mode(self):
        if self.get_device_os() == "windows":
            return self.docker_tcp_mode()
        else:
            return container_engine.connect_mode

    @staticmethod
    def docker_socket_mode():
        return "socket"

    @staticmethod
    def docker_socket_path():
        return container_engine.socket_path

    @staticmethod
    def docker_tcp_mode():
        return "tcp"

    @staticmethod
    def docker_api_port():
        return container_engine.api_port

    @staticmethod
    def docker_api_host():
        return container_engine.api_host

    @staticmethod
    def container_deploy_network_mode():
        return container_engine.network_mode

    @staticmethod
    def get_device_os():
        return platform.system().lower()

    @staticmethod
    def generate_id(prefix):
        if not prefix:
            prefix = "DATA_"
        _id = prefix
        timestamp = time.time()
        rand = random.randint(1000, 9999)
        _id += str(int(timestamp)) + "_" + str(rand)
        return _id

    @staticmethod
    def generate_uid():
        return str(uuid1()).split("-")[0] + str(time.time()).split(".")[0]
