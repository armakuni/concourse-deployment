#!/bin/sh
pip install -r concourse-deployment/ci/create-teams/requirements.txt

python concourse-deployment/ci/create-teams/task.py
