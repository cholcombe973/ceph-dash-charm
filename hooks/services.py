#!/usr/bin/python

from charmhelpers.core.services.base import ServiceManager
from charmhelpers.core.services import helpers

import actions

class CephContext(OSContextGenerator):
    """Generates context for /etc/ceph/ceph.conf templates."""
    interfaces = ['ceph']

    def __call__(self):
        if not relation_ids('ceph'):
            return {}

        log('Generating template context for ceph', level=DEBUG)
        mon_hosts = []
        auth = None
        key = None
        use_syslog = str(config('use-syslog')).lower()
        for rid in relation_ids('ceph'):
            for unit in related_units(rid):
                auth = relation_get('auth', rid=rid, unit=unit)
                key = relation_get('key', rid=rid, unit=unit)
                ceph_pub_addr = relation_get('ceph-public-address', rid=rid,
                                             unit=unit)
                unit_priv_addr = relation_get('private-address', rid=rid,
                                              unit=unit)
                ceph_addr = ceph_pub_addr or unit_priv_addr
                ceph_addr = format_ipv6_addr(ceph_addr) or ceph_addr
                mon_hosts.append(ceph_addr)

        ctxt = {'mon_hosts': ' '.join(sorted(mon_hosts)),
                'auth': auth,
                'key': key,
                'use_syslog': use_syslog}

        if not os.path.isdir('/etc/ceph'):
            os.mkdir('/etc/ceph')

        if not context_complete(ctxt):
            return {}

        ensure_packages(['ceph-common'])
        return ctxt

def manage():
    manager = ServiceManager([
        {
            'service': 'ceph-dash',
            'ports': [80],  # ports to after start
            'provided_data': [
                # context managers for provided relations
                # e.g.: helpers.HttpRelation()
            ],
            'required_data': [
                # data (contexts) required to start the service
                # e.g.: helpers.RequiredConfig('domain', 'auth_key'),
                #       helpers.MysqlRelation(),
            ],
            'data_ready': [
                helpers.render_template(
                    source='upstart.conf',
                    target='/etc/init/ceph-dash'),
                actions.log_start,
            ],
        },
    ])
    manager.manage()

if __name__ == '__main__':
    manage()
