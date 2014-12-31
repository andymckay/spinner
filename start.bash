# Start up docker, ensure data is in /mkt
echo 'starting' >> ~/.spinner.status
sudo service docker start

export FIG_FILE=~/.mkt.fig.yml
export FIG_PROJECT_NAME=mkt

echo 'building' >> ~/.spinner.status
fig up

echo 'complete' >> ~/.spinner.status
