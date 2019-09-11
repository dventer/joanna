from netmiko import Netmiko
from datetime import datetime
from time import sleep
import paramiko


class Network:
    def __init__(self, username, password=None, keys=None):
        '''
        :param username: username of device
        :param password: password of device
        :param keys: boolean
        '''
        self.username = username
        self.password = password
        self.keys = keys

    def command_cisco(self, hosts, set_command):
        HOST = {
                    'ip' : hosts,
                    'username' : self.username,
                    'password' : self.password,
                    'use_keys' : self.keys,
                    'device_type' : 'cisco_ios',
            }
        try:
            net_connect = Netmiko(**HOST)
            if isinstance(set_command, list):
                result = []
                for command in set_command:
                    result.append(net_connect.send_command(command))
                return result
            else:
                return net_connect.send_command(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")


    def command_firewall(self, hosts, set_command):
        HOST = {
                'ip' : hosts,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'fortinet',
        }
        try:
            net_connect = Netmiko(**HOST)
            return net_connect.send_command(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")


    def command_slb(self,host, set_command):
        HOST = {
            'ip': hosts,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'piolink',
        }
        try:
            net_connect = Netmiko(**HOST)
            return net_connect.send_command(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")

    def config_cisco(self, host, set_command):
        HOST = {
                'ip' : host,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'cisco_ios',
        }
        try:
            net_connect = Netmiko(**HOST)
            if isinstance(set_command, list):
                result = []
                for command in set_command:
                    result.append(net_connect.send_config_set(command))
                return result
            else:
                return net_connect.send_config_set(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")

    def config_file(self, host, set_file):
        HOST = {
                'ip' : host,
                'username' : self.username,
                'password' : self.password,
                'use_keys' : self.keys,
                'device_type' : 'cisco_ios',
        }
        net_connect = Netmiko(**HOST)
        return net_connect.send_config_from_file(set_file)

    def cisco_shell(self, host, set_command):
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=self.username, password=self.password)
        fshell = client.invoke_shell()
        fshell.send('terminal length 0\n')
        fshell.recv(6500)
        sleep(1)
        if isinstance(set_command, list):
            for command in set_command:
                fshell.send(command + '\n')
                sleep(3)
        else:
            fshell.send(set_command + '\n')
            sleep(3)

        cmd_output = fshell.recv(65000)
        return cmd_output.decode(encoding='UTF-8')
        client.close()


    def config_file(self, device, command):
        net_connect = Netmiko(**device)
        sleep(1)
        net_connect.send_config_from_file(command)
        sleep(1)
        print( device['ip'] + ' Done')


