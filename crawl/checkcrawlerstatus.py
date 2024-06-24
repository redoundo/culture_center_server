import subprocess
import json
from dotenv import load_dotenv
import os
load_dotenv()


def get_container_status(container):
    """
    container 상태를 반환
    """
    result = subprocess.run(['docker', 'inspect', container], stdout=subprocess.PIPE)
    container_info = json.loads(result.stdout.decode('utf-8'))
    if len(container_info) > 0:
        return container_info[0]['State']['Status']
    else:
        return None


def start_container_when_exit():
    """
    exit, pause 상태일 때만 container 를 실행시킨다.
    """
    container: str = "crawl_container"
    status = get_container_status(container)
    if status is None:
        return
    elif status != "Up":
        user_name: str = os.getenv("DOCKER_HUB_USERNAME")
        password: str = os.getenv("DOCKER_HUB_PASSWORD")
        subprocess.run(['docker', 'login', '-u', user_name, '-p', password])
        subprocess.run(['docker', 'container', 'start', container])
    return


if __name__ == "__main__":
    start_container_when_exit()






