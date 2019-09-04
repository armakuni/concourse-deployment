#!/bin/sh

# Installing Git
apt-get update
apt-get install -y git

# Install Python dependencies
pip install -r concourse-deployment/ci/create-teams-pipelines/requirements.txt

# Create SSH key file
# echo $GIT_PRIVATE_KEY > ~/.ssh/asdkjas

# Run Python script
python concourse-deployment/ci/create-teams-pipelines/task.py $CONCOURSE_URL $CONCOURSE_USERNAME $CONCOURSE_PASSWORD
