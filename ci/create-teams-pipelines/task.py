#!/usr/bin/env python

import yaml
import os
import sys
import subprocess
from git.repo.base import Repo


CONCOURSE_URL=sys.argv[1]
CONCOURSE_USERNAME=sys.argv[2]
CONCOURSE_PASSWORD=sys.argv[3]
BASE_CI_PATH = "concourse-deployment/ci/create-teams-pipelines/"
REPOSITORIES_LIST_FILE = BASE_CI_PATH + "repositories_list.yml"
TEAMS_CONFIG_FILE = BASE_CI_PATH + "teams-config.yml"


def process_yaml(yaml_file):
  with open(yaml_file, 'r') as stream:
    try:
        data_loaded = yaml.safe_load(stream)
        metadata = {}
        for data in data_loaded:
          for teams_key,teams_value in data.items():
            metadata[teams_key] = teams_value['repositories']
        return metadata
    except yaml.YAMLError as exc:
        print(exc)


def get_teams(metadata):
  return metadata.keys()


def get_repositories_from_team(metadata, team):
  return metadata[team]


def create_target(target, team, concourse_url, concourse_username, concourse_password):
  print("Creating Target: " + target)
  command = "fly login"
  command += " --verbose"
  command += " --insecure"
  command += " --target " + target
  command += " --concourse-url " + concourse_url
  command += " --username " + concourse_username
  command += " --password " + concourse_password
  command += " --team-name " + team
  os.system(command)


def create_team(target, team):
  print("Creating Team: " + team)
  command = "fly set-team"
  command += " --verbose "
  command += " --non-interactive"
  command += " --target " + target
  command += " --team-name " + team
  command += " --config " + TEAMS_CONFIG_FILE
  os.system(command)


def print_fly_targets():
  print("Fly Targets")
  os.system("fly targets")


def set_pipeline(path, target, pipeline_name, pipeline_config_path, pipeline_vars_paths):
  print("Setting pipeline: " + pipeline_name)
  
  # os.chdir(path) 
  
  command = "fly set-pipeline"
  command += " --verbose"
  command += " --target " + target
  command += " --pipeline " + pipeline_name
  command += " --config " + pipeline_config_path
  for vars_path in pipeline_vars_paths:
    command += " --load-vars-from " + vars_path
  
  print("     Command to Set Pipeline: " + command) # REMOVE THIS LINE
  # os.system(command)


data = process_yaml(REPOSITORIES_LIST_FILE)
teams = get_teams(data)
for team in teams:
  target = team

  target_created = create_target(target, team, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD)
  
  team_created = create_team(target, team)
  
  print_fly_targets()
  
  for repository in get_repositories_from_team(data, team):
    path = team + "-" + repository['pipeline_name']
    print("     Cloning Repository: " + repository['url'])
    # Repo.clone_from(repository['url'], path)
    pipeline_created = set_pipeline(path, target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'])
    # os.system("rm -rf " + path)