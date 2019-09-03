from network import Network
from datetime import datetime
from time import sleep
import os
import errno

now = datetime.now()
path = f'/opt/backup/{now:%d-%m-%Y}/'

try:
    os.mkdir(path)
except OSError as exc:
    if exc.errno != errno.EEXIST:
        raise


def backup_cisco():
    init = Network('jefri', keys=True)
    for host in ['bsd-core-a', 'bsd-core-b', 'bsd-dsw-a', 'bsd-dsw-b', 'bsd-banksw-a',
                 'bsd-banksw-b', 'bsd-asw-ext-a', 'bsd-asw-ext-b', 'bsd-asw-dmz-a', 'bsd-asw-dmz-b',
                 'bsd-asw-dev-a', 'bsd-asw-dev-b', 'bsd-asw-sync-a', 'bsd-asw-sync-b', 'bsd-rac-a',
                 'bsd-rac-b', 'bsd-mgmt-sw1', 'bsd-mgmt-sw2']:
        file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}', "w")
        file.write(init.command_cisco(host, 'sh run'))
        sleep(3)
        file.close()

def backup_mgmt():
    init = Network('cisco-backup','Cisco@Backup12#', keys=False)
    for host in ['bsd-asw-mgmt3','bsd-asw-mgmt4']:
        file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}', "w")
        file.write(init.command_cisco(host, 'sh run'))
        sleep(3)
        file.close()

def backup_forti():
    init = Network('jefri',keys=True)
    for host in ['bsd-fw','bsd-ext-fw']:
        file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}',"w")
        file.write(init.command_firewall(host, 'sh full'))
        sleep(3)
        file.close()

def backup_lb():
    init = Network('slb-backup','Nice@Backup12#', keys=False)
    for host in ['slb-int-a', 'slb-int-b', 'slb-dmz-a', 'slb-dmz-b', 'slb-ext-a', 'slb-ext-b']:
            file = open(f'/opt/backup/{now:%d-%m-%Y}/{host.upper()}_{now:%d%m%Y}',"w")
            sleep(3)
            file.write(init.command_slb(host, 'sh full'))
            file.close()


backup_cisco()
backup_mgmt()
backup_forti()
backup_lb()