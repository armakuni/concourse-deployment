# Concourse Deployment and Pipelines Setup

## Deploy Concourse

More information inside deployment folder.

## Setup Pipeline Creator for the first time.

1. Download `fly` tool.

        MacOS: https://<CONCOURSE_URL>/api/v1/cli?arch=amd64&platform=darwin
        Linux: https://<CONCOURSE_URL>/api/v1/cli?arch=amd64&platform=linux
        Windows: https://<CONCOURSE_URL>/api/v1/cli?arch=amd64&platform=windows

2. Put the `fly` file somewhere in your path

3. Login to Concourse server.

        fly login --target ak-concourse --concourse-url <CONCOURSE_URL>

4. Set the pipeline.

        fly set-pipeline --target ak-concourse --pipeline pipelines-creator --config ci/pipeline.yml --load-vars-from private/pipeline-secrets.yml

5. When `pipeline-creator` pipeline runs it will go through the list of teams and repositories declared in the file `ci/create-teams-pipelines/repositories_list.yml` and will set each of the pipelines.

## Add a new pipeline from a repository

1. Locate and open the file `ci/create-teams-pipelines/repositories_list.yml`.

2. if you want to add the pipeline into a new team add the following lines at the end of the file.

          - <TEAM_NAME>:
            repositories:
              - url: <REPOSITORY_URL_FOR_SSH_CLONE>
                pipeline_name: <PIPELINE_NAME>
                pipeline_config_path: <PATH_TO_PIPELINE_CONFIG>
                pipeline_vars_path: [ <PATH_TO_VARIABLES_FILE> ]

3. If you want to add your pipeline to an existing team, locate the team in the file and the repository fields under repositories tag.
        
          - url: <REPOSITORY_URL_FOR_SSH_CLONE>
              pipeline_name: <PIPELINE_NAME>
              pipeline_config_path: <PATH_TO_PIPELINE_CONFIG>
              pipeline_vars_path: [ <PATH_TO_VARIABLES_FILE> ]

4. Submit your changes and the `pipeline-creator` will setup your new pipeline.