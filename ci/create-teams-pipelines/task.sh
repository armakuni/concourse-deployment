#!/bin/sh

# Installing git and wget
apt-get update -qq
apt-get install -qq -y git wget git-crypt jq unzip

# Getting fly tool
wget --no-check-certificate -O fly "$CONCOURSE_URL/api/v1/cli?arch=amd64&platform=linux"
mv fly /usr/local/bin
chmod +x /usr/local/bin/fly
echo "Fly Version: $(fly --version)"

# Install 1Password CLI
wget -O op-cli.zip https://cache.agilebits.com/dist/1P/op/pkg/v0.6.1/op_linux_amd64_v0.6.1.zip
unzip op-cli.zip -d /tmp/op-cli
mv /tmp/op-cli/op /usr/local/bin
chmod +x /usr/local/bin/op
rm -rf op-cli.zip /tmp/op-cli

# Install Python dependencies
pip install -r concourse-deployment/ci/create-teams-pipelines/requirements.txt

# Create SSH key file
mkdir ~/.ssh
echo "$GIT_PRIVATE_KEY" > ~/.ssh/github_rsa
cat >> ~/.ssh/config <<EOL
Host bitbucket.org
 IdentityFile ~/.ssh/github_rsa

Host github.com
 IdentityFile ~/.ssh/github_rsa
EOL

chmod 600 ~/.ssh/github_rsa
eval "$(ssh-agent -s)"
ssh-add ~/.ssh/github_rsa

#Login 1password

eval $(echo "$ONEPASSWORD_MASTER" | op signin $ONEPASSWORD_SUBDOMAIN $ONEPASSWORD_ACCOUNT $ONEPASSWORD_SECRET)

# Run Python script
python concourse-deployment/ci/create-teams-pipelines/task.py $CONCOURSE_URL $CONCOURSE_USERNAME $CONCOURSE_PASSWORD $CONCOURSE_MAIN_TARGET $OP_SESSION_armakuni
