#!/usr/bin/env python
import sys
import subprocess
import re
import socket
import os
import pwd
import yaml

import gravelnode

import ssh_utils

def main():
    if len(sys.argv) != 2:
        sys.exit('usage: gravelregister <master hostname>')

    key = os.path.expanduser('~gravelnode/.ssh/id_rsa')
    hostname = 'gravelmaster@' + sys.argv[1]
    master_ssh_key = ssh_utils.call(hostname, 'get', 'ssh_public_key', key=key)
    ssh_utils.write_authorized_keys([('gravelmastercmd', master_ssh_key)], user='gravelnode')
    pw = pwd.getpwnam('gravelnode')
    os.chown(key, pw.pw_uid, pw.pw_gid)
    os.chown(os.path.dirname(key), pw.pw_uid, pw.pw_gid)
    os.chown(os.path.dirname(key) + '/authorized_keys', pw.pw_uid, pw.pw_gid)

    self_address = try_adresses(hostname, key)

    gravelnode.settings.data.master = sys.argv[1]
    gravelnode.settings.save()

    adjust_repo_path()

def adjust_repo_path():
    path = '/gravel/pkg/config.yaml'
    conf = yaml.load(open(path))
    conf['repo'] = 'ssh://' + gravelnode.master_ssh_addr()
    with open(path, 'w') as f:
        yaml.dump(conf, f)

def try_adresses(hostname, key):
    port = get_ssh_port()
    print 'SSH port:', port
    for ip in get_public_addresses():
        address = revdns(ip)
        print 'trying', ip, 'rev:', address
        address += ':' + port
        try:
            ssh_utils.call(hostname, 'setaddress', address, key=key)
        except subprocess.CalledProcessError:
            pass
        else:
            print 'address', address, 'set'
            return
    sys.exit('none of addresses worked')

def revdns(ip):
    if ip.startswith(('192.168.', '10.')):
        return ip
    try:
        return socket.gethostbyaddr(ip)[0]
    except socket.error:
        return ip

def get_ssh_port():
    conf = open('/etc/ssh/sshd_config').read().splitlines()
    for line in conf:
        m = re.match('^Port (\\d+)$', line)
        if m: return m.group(1)
    return '22'

def get_public_addresses():
    def key(address):
        if address.startswith(('192.168.', '10.')):
            return 1
        else:
            return 0

    return [ adr for adr in sorted(get_addresses()) if not adr.startswith('127.') ]

def get_addresses():
    output = subprocess.check_output(r"ip ad | grep -o -P '(\d{1,3}\.){3}(\d{1,3})/\d{1,2}'",
                                   shell=True)
    return [ adr.split('/')[0] for adr in output.splitlines() ]

if __name__ == '__main__':
    main()
