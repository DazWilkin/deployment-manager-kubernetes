### Introduction ###

Google [Cloud Deployment Manager](cloud.google.com/deployment-manager) can be used to provision any GCP resources.

With [Type Providers](https://cloud.google.com/deployment-manager/docs/configuration/type-providers/process-adding-api), Deployment Manager can provision all 3rd-party API.

This repo shows how to do this using Kubernetes API, enabling Deployment Manager to not only provision Kubernetes Engine clusters but to then deploy (Deployment|Service) to the cluster.

### Setup ###

Clone the repo

Create a GCP project and enable Deployment Manager:
```
gcloud services enable deploymentmanager.googleapis.com \
--project=${PROJECT}
```

Two of the scripts are intertwined. This is so that the script that creates Kubernetes Engine clusters (kubernetes_engine.py) can provide the cluster's master's endpoint IP to the script that creates the Kubernetes Engine types (kubernetes_engine_api.py). These are joined by a config file:
```
NAME=[[SOME-NAME]]
gcloud deployment-manager deployments create ${NAME} \
--config=generate_apis.yaml \
--project=${PROJECT}
```

This will create a Kubernetes cluster (${NAME}) and 3 distinct types:
```
kubernetes
kubernetes-app
kubernetes-v1beta1-extensions
```

Then you can create a Deployment and Service on the cluster with, e.g.:
```
gcloud deployment-manager deployments create k \
--template=deployment.py \
--project=${PROJECT} \
--properties=\
name:henry,\
port:80,\
image:nginx
```

### Tidy Up ###

Delete the cluster either directly or using Deployment Manager:
```
gcloud deployment-manager deployments delete ${NAME} \
--project=${PROJECT}
```

NB While you can delete the Kubernetes deployment, this only deletes the Kubernetes Service and does not (for some reason) delete the Kubernetes Deployment.