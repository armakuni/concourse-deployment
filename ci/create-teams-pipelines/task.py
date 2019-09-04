#!/usr/bin/env python

import yaml
import os
from git.repo.base import Repo


BASE_CI_PATH = "ci/create-teams-pipelines/"
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


def create_target_command(target):
  concourse_url = 'asd'
  username = 'asd'
  password = 'asd'

  command = "fly login"
  command += " --target " + target
  command += " --concourse-url " + concourse_url
  command += " --username " + username
  command += " --password " + password
  command += " --team-name " + target
  command += " --insecure"
  return command


def create_team_command(target):
  command = "fly set-team --non-interactive "
  command += "--target " + target
  command += " --team-name " + target
  command += " --config " + TEAMS_CONFIG_FILE
  return command


def create_set_pipeline_command(target, pipeline_name, pipeline_config_path, pipeline_vars_paths):
  command = "fly set-pipeline"
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
  command_to_create_target = create_target_command(target)
  print("Command to Create Target: " + command_to_create_target) # REMOVE THIS LINE
  #os.system(command_to_create_target)
  command_to_create_team = create_team_command(target)
  print("Command to Create Team: " + command_to_create_team)
  # os.system(command_to_create_team)
  for repository in get_repositories_from_team(data,team):
    path = team + "-" + repository['pipeline_name']
    print("     Cloning Repository: " + repository['url'])
    # Repo.clone_from(repository['url'], path)
    command_to_set_pipeline = create_set_pipeline_command(target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'])
    print("     Command to Set Pipeline: " + command_to_set_pipeline) # REMOVE THIS LINE
    # os.system(command)
    # os.system("rm -rf " + path)
