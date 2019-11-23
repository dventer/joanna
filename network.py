from netmiko import Netmiko
from time import sleep
import paramiko


class Network:
    def __init__(self, username, password=None, keys=True):
        '''
        :param username: username of device
        :param password: password of device
        :param keys: boolean
        '''
        self.username = username
        self.password = password
        self.keys = keys

    def command_cisco(self, hosts, set_command):
        '''

        :param hosts: hostname or IP of the device
        :param set_command: command send to device, can be string or list
        :return:
        '''
        device = {
            'ip': hosts,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'cisco_ios',
        }
        try:
            net_connect = Netmiko(**device, fast_cli=True)
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
        device = {
            'ip': hosts,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'fortinet',
        }
        try:
            net_connect = Netmiko(**device, fast_cli=True)
            if isinstance(set_command, list):
                result = []
                for command in set_command:
                    result.append(net_connect.send_command(command))
                return result
            else:
                return net_connect.send_command(set_command, auto_find_prompt=False)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")

    def command_slb(self, host, set_command):
        device = {
            'ip': host,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'piolink',
        }
        try:
            net_connect = Netmiko(**device)
            return net_connect.send_command(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")

    def config_cisco(self, host, set_command):
        device = {
            'ip': host,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'cisco_ios',
        }
        try:
            net_connect = Netmiko(**device)
            net_connect.send_config_set(set_command)
        except paramiko.ssh_exception.AuthenticationException:
            print("\nWrong Password\n")

    def config_file(self, host, set_file):
        '''
        this method can be use if you want to write the command in file
        :param host: IP or hostname the device
        :param set_file: file location that contain some command
        :return:
        '''
        device = {
            'ip': host,
            'username': self.username,
            'password': self.password,
            'use_keys': self.keys,
            'device_type': 'cisco_ios',
        }
        net_connect = Netmiko(**device)
        return net_connect.send_config_from_file(set_file)

    def cisco_shell(self, host, set_command):
        '''
        This is shell prompt, it will be usefull for gather evidence to controlcase
        :param host:
        :param set_command:
        :return:
        '''
        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        client.connect(host, username=self.username, password=self.password)
        fshell = client.invoke_shell()
        fshell.send('terminal length 0\n')
        output = ''
        sleep(1)
        fshell.recv(6500)
        if isinstance(set_command, list):
            for command in set_command:
                fshell.send(command + '\n')
                sleep(2.5)
        else:
            fshell.send(set_command + '\n')
            sleep(1.5)
        while True:
            msg = fshell.recv(16)
            if len(msg) <= 0:
                break
            output += msg.decode("utf-8")
        cmd_output = fshell.recv(65000)
        return cmd_output.decode(encoding='UTF-8')
        client.close()
