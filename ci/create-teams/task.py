#!/usr/bin/env python

import yaml
import sys
import os
from git.repo.base import Repo


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
  command = "fly login --insecure"
  comand += " --target " + target
  comand += " --concourse-url " + concourse_url
  comand += " --username " + username
  comand += " --password " + password
  return command


def create_team_command(target):
  command = "fly --target " + target + " set-team --non-interactive"
  command += " --team-name " + target
  command += " --github-team armakuni:concourse-ak-software"
  command += " --bitbucket-cloud-team armakuni"
  return command


def create_set_pipeline_command(target, pipeline_name, pipeline_config_path, pipeline_vars_paths):
  command = "fly --target " + target + " set-pipeline"
  command += " --pipeline " + pipeline_name
  command += " --config " + pipeline_config_path
  for vars_path in pipeline_vars_paths:
    command += " --load-vars-from " + vars_path
  return command


data = process_yaml("repositories_list.yaml")
teams = get_teams(data)
for team in teams:
  os.system('fly --version')
  # Check if target exists
  # Create target
    # target = team
    # command_to_create_target = create_target_command(target)
    # os.system(command_to_create_target)
  # Check if Team exists
  # Create the team
    # command_to_create_team = create_team_command(target)
    # os.system(command_to_create_team)
  for repository in get_repositories_from_team(data,team):
    os.system('fly --version')
    # path = team + "-" + repository['pipeline_name']
    # Repo.clone_from(repository['url'], path)
    # command = create_set_pipeline_command(target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'])
    # os.system(command)
    # os.system("rm -rf " + path)