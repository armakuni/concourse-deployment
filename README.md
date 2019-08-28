# Concourse Deployment (Control Tower)

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
