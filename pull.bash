echo 'pulling' >> ~/.spinner.status
# Ensure that selinux allows access to the directories.
# See http://stackoverflow.com/questions/24288616/permission-denied-on-accessing-host-directory-in-docker
sudo chcon -Rt svirt_sandbox_file_t /mkt

# Pull the projects down from github.
sudo easy_install pip
sudo pip install marketplace-env
mkdir /mkt/projects
mkt root /mkt/projects
mkt whoami mozilla
mkt checkout
echo 'pulling done' >> ~/.spinner.status
