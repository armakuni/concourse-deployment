#!/bin/sh

# Installing git and wget
apt-get update -qq
apt-get install -qq -y git wget

# Getting fly tool
wget --no-check-certificate -O fly "$CONCOURSE_URL/api/v1/cli?arch=amd64&platform=linux"
mv fly /usr/local/bin
chmod +x /usr/local/bin/fly
echo "Fly Version: $(fly --version)"

# Install Python dependencies
pip install -r concourse-deployment/ci/create-teams-pipelines/requirements.txt

mkdir ~/.ssh

# Create SSH key file
ssh -V
sshd -V
echo $GIT_PRIVATE_KEY > ~/.ssh/github_rsa
chmod 600 ~/.ssh/github_rsa
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_rsa


# Run Python script
python concourse-deployment/ci/create-teams-pipelines/task.py $CONCOURSE_URL $CONCOURSE_USERNAME $CONCOURSE_PASSWORD
