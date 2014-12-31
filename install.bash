echo 'starting' >> ~/.spinner.status
# Attach the /mkt partition where we'll store our stuff.
sudo mkfs -t ext4 /dev/xvdb
sudo mkdir /mkt
sudo chown -R ec2-user:ec2-user /mkt
sudo mount /dev/xvdb /mkt

echo 'installing' >> ~/.spinner.status
# Install all the things.
sudo yum install -y gcc python-devel npm gcc-c++ make openssl-devel

# Install Docker, move it over to the /mkt partition.
sudo yum install yum-utils
sudo yum-config-manager --enable rhui-REGION-rhel-server-extras
sudo rm -r /var/lib/docker
mkdir /mkt/docker
sudo ln -s /mkt/docker /var/lib
sudo yum install -y docker
# Ensure that ec2-user is in the docker group.
sudo usermod -a -G docker ec2-user

echo 'install done' >> ~/.spinner.status
