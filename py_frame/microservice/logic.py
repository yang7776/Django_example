# -*- coding: utf-8 -*-

import platform
import socket
import psutil
import common.mylog as logging
from common import settings
from task.utils import get_agent_uuid, get_host_ips
from utils import distro

logger = logging.getLogger(__name__)

OS_TYPE = {
    'Windows': 1,
    'Linux': 2,
    'Darwin': 3
}


def get_device_info():
    try:
        if platform.system() == 'Linux':
            os_version = distro.os_release_info().get('pretty_name')
        else:
            os_version = f'{platform.release()}-{platform.machine()}'
        worker = {
            "agent_type": settings.AGENT_TYPE,
            "uuid": get_agent_uuid().strip(),
            "ip": get_host_ips(),
            "os_type": OS_TYPE[platform.system()],
            "os_version": os_version,
            "status": "1",
            "version": settings.CONTAINER_VERSION,
            "create_by": settings.SECKER_API_USER,
        }
        logger.info(f'Agent Register Info: {worker}')
        return True, worker
    except Exception as e:
        logger.error(f'Agent Register Error: {e}', exc_info=True)
        return False, {}


def get_system_info():
    memory = {}
    cpu = {}
    serverPort = {}
    depend_data = {}
    server_list = ["http", "tomcat", "secker-agent"]
    try:
        for server_name in server_list:
            port = socket.getservbyname(server_name)
            serverPort[server_name] = port
    except Exception as e:
        logger.error(f'get server port error：{e}')

    try:
        with open(settings.REQUIRE_PATH, "r") as f:
            for _ in f:
                d = _.strip().split("==")
                depend_data[d[0]] = d[1]
    except Exception as e:
        logger.error(f"depend report error : {e}")

    cpu['logical_count'] = psutil.cpu_count()
    cpu['physics_count'] = psutil.cpu_count(logical=False)
    cpu['cpu_percent'] = psutil.cpu_percent()

    mem = psutil.virtual_memory()
    memory['free'] = int(mem.free / 1024 / 1024)
    memory['total'] = int(mem.total / 1024 / 1024)

    data = {
        "cpu": cpu,
        "version": settings.CONTAINER_VERSION,
        "memory": memory,
        "agent_type": settings.AGENT_TYPE,
        "uuid": get_agent_uuid().strip(),  # agent标识
        "serverPort": serverPort,
        "depend_data": depend_data,
    }
    return True, data


def get_version():
    return True, {"version":settings.CONTAINER_VERSION}


def upload_file(file_type):
    data = {"msg":"上传成功"}
    flag = True
    if file_type == "agent":
        pass
    elif file_type == "scene":
        pass
    else:
        flag = False
        data["msg"] = "type not exist!"
    return flag, data
