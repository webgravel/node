import sys
sys.path.append('/gravel/pkg/gravel-common')

import graveldb

PATH = '/gravel/system/node'

class Settings(graveldb.Table('settings', PATH)):
    default = dict()

    def __init__(self):
        super(Settings, self).__init__('settings')

settings = Settings()

def master_ssh_addr():
    return 'gravelmaster@' + settings.data.master
