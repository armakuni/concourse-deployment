# Deploy Concourse on AWS EKS





## Configure Helm

1. Install Helm on MacOS

        brew install kubernetes-helm

2. Configure Helm access with RBAC

        kubectl apply -f rbac.yaml

3. Install tiller using the helm tooling
    
        helm init --service-account tiller

## Concourse

Read carefully this documentation to install Concourse in he right way: https://hub.kubeapps.com/charts/stable/concourse

1. Edit values.yaml to use the correct options

2. Install Concourse

        helm install --name <NAME> -f values.yaml stable/concourse

3. Delete Concourse

        helm delete <NAME>

4. Cleanup orphaned Persistent Volumes

        kubectl delete pvc -l app=<NAME>-worker