from ..config.services import services
from random import randint


def random_pick_a_service(env):
    if env not in services:
        raise ValueError("wrong env = %s" % env)
    service_ip_list = services[env]
    return service_ip_list[randint(0, len(service_ip_list) - 1)]


