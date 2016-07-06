import requests
import datetime

from pecan import conf
from sqlalchemy import asc

from shaman import models


def get_next_node():
    """
    Retrieves the next chacra node in
    the rotation and returns it.
    """
    next_node = models.Node.query.filter_by(healthy=True).order_by(asc(models.Node.last_used)).first()
    if not next_node:
        # maybe raise an exception here?
        return None
    if is_node_healthy(next_node):
        return next_node
    else:
        # look again to find a healthy node
        return get_next_node()


def is_node_healthy(node):
    check_url = "https://{}/health/".format(node.host)
    r = requests.get(check_url)
    node.last_check = datetime.datetime.now()
    models.commit()
    if r.status_code == 200:
        return True
    else:
        node.down_count = node.down_count + 1
        if node.down_count == conf.health_check_retries:
            node.healthy = False
        models.commit()

    return False
