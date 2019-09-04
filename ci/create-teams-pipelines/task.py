#!/usr/bin/env python

import yaml
import os
import sys
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


def create_target_command(target, team, concourse_url, concourse_username, concourse_password):
  command = "fly login"
  command += " --verbose"
  command += " --target " + target
  command += " --concourse-url " + concourse_url
  command += " --username " + concourse_username
  command += " --password " + concourse_password
  command += " --team-name " + team
  command += " --insecure"
  return command


def create_team_command(target, team):
  command = "fly set-team --non-interactive "
  command += " --verbose"
  command += "--target " + target
  command += " --team-name " + team
  command += " --config " + TEAMS_CONFIG_FILE
  return command


def create_set_pipeline_command(target, pipeline_name, pipeline_config_path, pipeline_vars_paths):
  command = "fly set-pipeline"
  command += " --verbose"
  command += "--target " + target
  command += " --pipeline " + pipeline_name
  command += " --config " + pipeline_config_path
  for vars_path in pipeline_vars_paths:
    command += " --load-vars-from " + vars_path
  return command



data = process_yaml(REPOSITORIES_LIST_FILE)
teams = get_teams(data)
for team in teams:
  target = team
  print("Creating Target: " + target)
  command_create_target = create_target_command(target, team, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD)
  print(command_create_target)
  os.system(command_create_target)
  
  print("Creating Team: " + team)
  command_create_team = create_team_command(target, team)
  print(command_create_team)
  os.system(command_create_team)
  
  print("Fly Targets")
  os.system("fly targets")
  
  for repository in get_repositories_from_team(data, team):
    path = team + "-" + repository['pipeline_name']
    print("     Cloning Repository: " + repository['url'])
    # Repo.clone_from(repository['url'], path)
    command_set_pipeline = create_set_pipeline_command(target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'])
    print("     Command to Set Pipeline: " + command_set_pipeline) # REMOVE THIS LINE
    # os.system(command_set_pipeline)
    # os.system("rm -rf " + path)
