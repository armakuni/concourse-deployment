#!/bin/sh
pip install -r concourse-deployment/ci/create-pipelines/requirements.txt

python concourse-deployment/ci/create-pipelines/task.py