#!/usr/bin/env python

import yaml
import os
import sys
import subprocess
from git.repo.base import Repo


CONCOURSE_URL=sys.argv[1]
CONCOURSE_USERNAME=sys.argv[2]
CONCOURSE_PASSWORD=sys.argv[3]
OP_SESSION_armakuni=sys.argv[4]
MAIN_CONCOURSE_TARGET = "ak-concourse-deployment"
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


def create_target(target, concourse_url, concourse_username, concourse_password, team = None):
  print("Creating Target: " + target)
  command = "fly login"
  command += " --insecure"
  command += " --target " + target
  command += " --concourse-url " + concourse_url
  command += " --username " + concourse_username
  command += " --password " + concourse_password
  if (team != None):
    command += " --team-name " + team
  os.system(command)


def create_team(target, team):
  print("Creating Team: " + team)
  command = "fly set-team"
  command += " --non-interactive"
  command += " --target " + target
  command += " --team-name " + team
  command += " --config " + TEAMS_CONFIG_FILE
  # command += " --local-user " + CONCOURSE_USERNAME
  os.system(command)


def set_pipeline(path, target, pipeline_name, pipeline_config_path, pipeline_vars_paths, pipeline_onepassword_key):
  print("Setting pipeline: " + pipeline_name)
  
  os.chdir(path)
  
  ps = subprocess.Popen(("op", "get", "item",  pipeline_onepassword_key, "--session=" + OP_SESSION_armakuni), stdout=subprocess.PIPE)
  Uuid = subprocess.check_output(("jq", ".uuid"), stdin=ps.stdout)
  ps.wait()
  
  os.system("op get document " + Uuid.decode('ascii') + "  &> gitkey.key")

  print("FILE GITKEY CONTENT:")
  os.system("cat gitkey.key")
   
  os.system("git-crypt unlock gitkey.key")

  command = "fly set-pipeline -n"
  command += " --target " + target
  command += " --pipeline " + pipeline_name
  command += " --config " + path + '/' + pipeline_config_path
  for vars_path in pipeline_vars_paths:
    command += " --load-vars-from " + vars_path
  
  print("     Command to Set Pipeline: " + command) # REMOVE THIS LINE
  os.system(command)


data = process_yaml(REPOSITORIES_LIST_FILE)
teams = get_teams(data)

# Create Main Concourse Target
main_target_created = create_target(MAIN_CONCOURSE_TARGET, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD)
# Print Fly Targets
print("Fly Targets")
os.system("fly targets")

os.system("touch ~/.ssh/known_hosts")
os.system("ssh-keyscan github.com >> ~/.ssh/known_hosts")
os.system("ssh-keyscan bitbucket.org >> ~/.ssh/known_hosts")


MAIN_DIRECTORY = os.getcwd()

for team in teams:
  target = team
  # Create Team using Main Concourse Target
  team_created = create_team(MAIN_CONCOURSE_TARGET, team)
  # Create new Target for the previously create Team
  target_created = create_target(target, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD, team)
  
  for repository in get_repositories_from_team(data, team):
    REPOSITORY_DIRECTORY = MAIN_DIRECTORY + "/" + team + "-" + repository['pipeline_name']
    print("     Cloning Repository: " + repository['url'])
    Repo.clone_from(repository['url'], REPOSITORY_DIRECTORY)
    pipeline_created = set_pipeline(REPOSITORY_DIRECTORY, target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'], repository['pipeline_onepassword_key'])
    os.chdir(MAIN_DIRECTORY)
    os.system("rm -drf " + REPOSITORY_DIRECTORY)
# Print Fly Targets
print("Fly Targets")
os.system("fly targets")
