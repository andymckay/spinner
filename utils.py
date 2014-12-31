import logging
import os
import sys
import time

import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance

log = logging.getLogger('spinner')

# Set up a 20gig partition.
def partition():
    dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType()
    dev_sda1.size = 20
    bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
    bdm['/dev/xvdb'] = dev_sda1
    return bdm


class Spinner(object):

    def __init__(self, instance_type, key_name, security_group, region, pem):
        self.instance_type = instance_type
        self.key_name = key_name
        self.security_group = security_group
        self.region = region
        self.pem = pem
        self.conn = boto.ec2.connect_to_region(region)

    def create(self):
        result = self.conn.run_instances(
            self.instance_type,
            key_name=self.key_name,
            instance_type='t2.medium',
            security_groups=['default', self.security_group],
            block_device_map=partition()
        )
        return result.instances[0]

    def find_running(self):
        running = []
        reservations = self.conn.get_all_reservations()
        for reservation in reservations:
            for i in reservation.instances:
                if i.state == 'running':
                    running.append(i)

        return running

    def find_state(self, instance):
        reservations = self.conn.get_all_reservations()
        for reservation in reservations:
            for i in reservation.instances:
                if i.id == instance.id:
                    return i.state

        raise ValueError('Instance: %s not found.' % (id))

    def wait_for(self, instance, state):
        for x in range(0, 10):
            if self.find_state(instance) == state:
                print 'Instance: %s is %s' % (instance.id, state)
                return

            time.sleep(5)
            sys.stdout.write('.')

        raise ValueError('Instance: %s did not report %s.'
                         % (instance.id, state))

    def wait_for_file(self, ssh, filename):
        for x in range(0, 10):
            if ssh.exists(filename):
                continue

            time.sleep(1)
            sys.stdout.write('.')

    def run_pty(self, ssh, cmd):
        log.debug('running: %s' % cmd)
        channel = ssh.run_pty(cmd)
        while not channel.exit_status_ready():
            log.debug(channel.recv(1024))

    def setup(self, instance):
        log.debug('running setup on instance id: %s' % instance.id)
        ssh = sshclient_from_instance(
            instance, self.pem, user_name='ec2-user')
        self.run_pty(ssh, 'sudo yum install -y git')
        self.wait_for_file(ssh, '/usr/bin/git')
        self.run_pty(ssh, 'git clone https://github.com/andymckay/spinner.git')
        self.wait_for_file(ssh, 'spinner/create.bash')
        self.run_pty(ssh, 'spinner/install.bash')
        self.run_pty(ssh, 'spinner/pull.bash')
        self.run_pty(ssh, 'spinner/start.bash')
