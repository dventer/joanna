# !/usr/sbin/python3.6
import paramiko
import getpass
import sys, os
import time

USERNAME = input('Username: ')
PASSWORD = getpass.getpass('Password: ')


def connect(host, command)
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    myshell = client.invoke_shell()
    banner = myshell.recv(6500)
    time.sleep(1)
    if 'sudo' in command:
        myshell.send(command + '\n')
    time.sleep(1)
    myshell.send(PASSWORD + '\n')
    time.sleep(1.5)
    cmd_output = myshell.recv(65535)
    print(cmd_output.decode(encoding='UTF-8'))


interface = sys.argv[1:-1]
command = sys.argv[-1]
if len(sys.argv) == 3:
    connect(sys.argv[1], command)
    print('\n\n')
else:
    for host in interface:
        connect(host, command)
        print('\n\n')