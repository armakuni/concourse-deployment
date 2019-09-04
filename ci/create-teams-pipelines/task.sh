#!/bin/sh

# Installing Git
apt-get update
apt-get install -y git

# Install Python dependencies
pip install -r concourse-deployment/ci/create-teams-pipelines/requirements.txt

echo "Concourse URL: $CONCOURSE_URL"
echo "Concourse Username: $CONCOURSE_USERNAME"
echo "Concourse Password: $CONCOURSE_PASSWORD"


# Create ssh key file
# echo $GIT_PRIVATE_KEY > ~/.ssh/asdkjas

# Run Python script
python concourse-deployment/ci/create-teams-pipelines/task.py
