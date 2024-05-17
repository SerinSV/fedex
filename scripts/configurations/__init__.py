from dotenv import load_dotenv
from pydantic import BaseSettings

load_dotenv()

class Ssh(BaseSettings):
    host: str
    port: int
    username: str
    password: str

    class Config:
        env_prefix = "SSH_"


class ContainerEngine(BaseSettings):
    connect_mode: str
    socket_path: str
    api_port: int
    network_mode: str
    api_host: str

    class Config:
        env_prefix = "CONTAINER_ENGINE_"

class Volume(BaseSettings):
    volume: str


ssh = Ssh()
container_engine = ContainerEngine()
volume = Volume()
