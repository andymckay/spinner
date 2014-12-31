echo 'fixing' >> ~/.spinner.status
# Fireplace points to mp.dev by default, we need to fix that.
cd /mkt/projects/fireplace
# Finds the IP for the public interface for this server.
IP=`curl -s ifconfig.me`
cp "src/media/js/settings_local.js.dist" "src/media/js/settings_local.js"
sed -i "" -e "s/https/http/g" -e "s/[a-z\-]*\.allizom\.org/$IP/g" "src/media/js/settings_local.js"
echo 'fixing done' >> ~/.spinner.status
