import os

import boto.ec2
from boto.manage.cmdshell import sshclient_from_instance


conn = boto.ec2.connect_to_region('us-west-2')
pem = os.path.expanduser('~/.aws/spinner-app.pem')


dev_sda1 = boto.ec2.blockdevicemapping.EBSBlockDeviceType()
dev_sda1.size = 20
bdm = boto.ec2.blockdevicemapping.BlockDeviceMapping()
bdm['/dev/sda1'] = dev_sda1

def create():
    result = conn.run_instances(
        'ami-99bef1a9',
        # Red Hat Enterprise Linux 7.0 (HVM), SSD Volume Type
        key_name='spinner-app',
        instance_type='t2.micro',
        security_groups=['default', 'spinner-app'],
        block_device_map=bdm
    )
    return result.instances[0]

def find_running():
    running = []
    reservations = conn.get_all_reservations()
    for reservation in reservations:
        for instance in reservation.instances:
            if instance.state == 'running':
                running.append(instance)
            else:
                print instance.state
    return running

def find():
    for instance in find_running():
        ssh = sshclient_from_instance(instance, pem)
        ssh.put_file('create.bash', '/home/ec2-user')
        ssh.run('chmod a+x create.bash')
        #status, stdout, stderr = ssh.run('./create.bash')
        #print status, stdout, stderr



if __name__=='__main__':
    #create()
    find()
