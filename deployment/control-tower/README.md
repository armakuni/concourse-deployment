# Concourse Deployment using Control Tower

## Usage

Run the container

        docker run --tty --interactive --env AWS_ACCESS_KEY_ID='<YOUR_AWS_ACCESS_KEY>' --env AWS_SECRET_ACCESS_KEY='<YOUR_AWS_SECRET_KEY>' --name control-tower jnonino/control-tower bash

After running that command you will prompted to the container environment, you can run the following Control Tower commands:

- **deploy**: Deploys or updates a Concourse ([Documentation](https://github.com/EngineerBetter/control-tower/blob/master/docs/deploy.md))
- **destroy**: Destroys a Concourse ([Documentation](https://github.com/EngineerBetter/control-tower/blob/master/docs/destroy.md))
- **info**: Fetches information on a deployed environment ([Documentation](https://github.com/EngineerBetter/control-tower/blob/master/docs/info.md))
- **maintain**: Handles maintenance operations in control-tower ([Documentation](https://github.com/EngineerBetter/control-tower/blob/master/docs/maintain.md))
- **help**: Get help for commands

More information [here](https://github.com/EngineerBetter/control-tower)

## Deploy

        control-tower deploy --iaas [AWS|GCP] <your-project-name>        

More help: https://github.com/EngineerBetter/control-tower/blob/master/docs/deploy.md

## Information

To fetch information about your Control Tower deployment in a human readable format:

        control-tower info --iaas [AWS|GCP] <your-project-name>

To fetch Information about your Control Tower deployment in a machine parseable format:

        control-tower info --iaas [AWS|GCP] --json <your-project-name>

To load credentials into your environment from your Control Tower deployment:

        eval "$(control-tower info --iaas [AWS|GCP] --env <your-project-name>)"

To check the expiry of the BOSH Director's NATS CA certificate:

        control-tower info --iaas [AWS|GCP] --cert-expiry <your-project-name>

More help: https://github.com/EngineerBetter/control-tower/blob/master/docs/info.md

## Destroy

        control-tower destroy --iaas [AWS|GCP] <your-project-name>