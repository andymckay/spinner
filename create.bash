sudo yum install -y docker gcc git python-devel npm gcc-c++ make openssl-devel
sudo easy_install pip
sudo pip install marketplace-env
mkdir marketplace
mkt root ~/marketplace/
mkt whoami mozilla
mkt checkout
sudo service docker start
export FIG_FILE=~/.mkt.fig.yml
export FIG_PROJECT_NAME=mkt
# Not sure about this but it means we dont need to sudo. This is bad
# right?
sudo chmod 0777 /var/run/docker.sock
fig up
