#!/usr/bin/env python

import yaml

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