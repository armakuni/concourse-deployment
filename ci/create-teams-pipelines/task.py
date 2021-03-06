#!/usr/bin/env python

import yaml
import os
import sys
import subprocess
from git.repo.base import Repo

CONCOURSE_URL=sys.argv[1]
CONCOURSE_USERNAME=sys.argv[2]
CONCOURSE_PASSWORD=sys.argv[3]
CONCOURSE_MAIN_TARGET = sys.argv[4]#"ak-concourse-cluster"
OP_SESSION_armakuni=sys.argv[5]
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
  print("------------------------ START Target: " + target + "-------------------------------")
  command = "fly login"
  command += " --insecure"
  command += " --target " + target
  command += " --concourse-url " + concourse_url
  command += " --username '" + concourse_username +"'"
  command += " --password '" + concourse_password +"'"
  if (team != None):
    command += " --team-name " + team
  os.system(command)
  print("------------------------ END Target: " + target + "-------------------------------\n\n")


def create_team(target, team):
  print("------------------------ START Team: " + team + "-------------------------------")
  command = "fly set-team"
  command += " --non-interactive"
  command += " --target " + target
  command += " --team-name " + team
  command += " --config " + TEAMS_CONFIG_FILE
 # command += " --local-user " + CONCOURSE_USERNAME
  os.system(command)
  print("------------------------ END Team: " + team  + "-------------------------------\n\n")


def set_pipeline(path, target, pipeline_name, pipeline_config_path, pipeline_vars_paths, pipeline_onepassword_key):
  print("Setting pipeline: " + pipeline_name)
  
  os.chdir(path)
  
  ps = subprocess.Popen(("op", "get", "item",  pipeline_onepassword_key, "--session=" + OP_SESSION_armakuni), stdout=subprocess.PIPE)
  Uuid = subprocess.check_output(("jq", ".uuid"), stdin=ps.stdout)
  uid = Uuid.decode('utf-8')
  #print("uuid = "+ uid)
  ps.wait()

  gkey = subprocess.check_output(("op",  "get", "document", uid.split('"')[1]), stdin=ps.stdout)

  fw = open("gitkey.key","wb+")
  fw.write(gkey)
  fw.close()

  #os.system("cat gitkey.key") 
   
  os.system("git-crypt unlock gitkey.key")

  #Set pipeline  
  command = "fly set-pipeline -n"
  command += " -t " + target
  command += " -p " + pipeline_name
  command += " -c " + path + '/' + pipeline_config_path
  # command += " -l " + pipeline_vars_paths[0]
  for vars_path in pipeline_vars_paths:
    command += " -l " + vars_path
  
  #print("     Command to Set Pipeline: " + command) # REMOVE THIS LINE
  os.system(command)


data = process_yaml(REPOSITORIES_LIST_FILE)
teams = get_teams(data)

# Create Main Concourse Target
main_target_created = create_target(CONCOURSE_MAIN_TARGET, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD)
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
  team_created = create_team(CONCOURSE_MAIN_TARGET, team)
  # Create new Target for the previously create Team
  target_created = create_target(target, CONCOURSE_URL, CONCOURSE_USERNAME, CONCOURSE_PASSWORD, team)
  
  for repository in get_repositories_from_team(data, team):
    print("------------------------ START PIPELINE: " + repository['pipeline_name'] + "-------------------------------")
    REPOSITORY_DIRECTORY = MAIN_DIRECTORY + "/" + team + "-" + repository['pipeline_name']
    print("     Cloning Repository: " + repository['url'])
    Repo.clone_from(repository['url'], REPOSITORY_DIRECTORY)
    pipeline_created = set_pipeline(REPOSITORY_DIRECTORY, target, repository['pipeline_name'], repository['pipeline_config_path'], repository['pipeline_vars_path'], repository['pipeline_onepassword_key'])
    os.chdir(MAIN_DIRECTORY)
    print("------------------------ END PIPELINE: " + repository['pipeline_name'] + "-------------------------------\n\n")
    #os.system("rm -drf " + REPOSITORY_DIRECTORY) #UNDO THIS COMMENTED LINE
# Print Fly Targets
print("Fly Targets")
os.system("fly targets")
