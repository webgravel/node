import sys
import os
sys.path.append('/gravel/pkg/gravel-common')

import graveldb
import ssh_utils

PATH = '/gravel/system/node'

class Settings(graveldb.Table('settings', PATH)):
    default = dict()

    def __init__(self):
        super(Settings, self).__init__('settings')

settings = Settings()

def master_ssh_addr():
    return 'gravelmaster@' + settings.data.master

def master_call(*args, **kwargs):
    _kwargs = dict(key=os.path.expanduser('~gravelnode/.ssh/id_rsa'))
    _kwargs.update(kwargs)
    return ssh_utils.call(master_ssh_addr(), *args, **_kwargs)
