from subprocess import check_output, CalledProcessError

from enum import Enum


__author__ = 'chris'


class CephClientType(Enum):
    client = 'client'
    osd = 'osd'
    mon = 'mon'
    mds = 'mds'


class CephBucketType(Enum):
    osd = 'osd'
    host = 'host'
    chassis = 'chassis'
    rack = 'rack'
    row = 'row'
    pdu = 'pdu'
    pod = 'pod'
    room = 'room'
    datacenter = 'datacenter'
    region = 'region'
    root = 'root'


def get_user(client_type, client_id):
    """
    :param client_type: Class CephClientType
    :param client_id: str
    :return: str
    """
    try:
        out = check_output(['ceph', 'auth', 'get', client_type + '.' + client_id]).decode('UTF-8')
        return out
    except CalledProcessError:
        return None


if __name__ == '__main__':
    print(get_user(CephClientType.client, 'admin'))
