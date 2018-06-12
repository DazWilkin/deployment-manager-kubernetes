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

### Local|Regional Clusters ###

There are 2 variants:
1. Zonal Cluster
1. [Regional Cluster](https://cloud.google.com/kubernetes-engine/docs/concepts/multi-zone-and-regional-clusters#regional)

A Zonal Cluster will be deployed in a single zone of your choosing, e.g. `us-west1-c`. A Regional Cluster will be deployed in 3 zones in a region of your choosing, e.g. `us-west1` (will create nodes in `us-west1-a`,`us-west1-b` and `us-west1-c`).

Set the environment variable `${VARIANT}` depending on which you'd prefer:

1. `VARIANT=zonal`
1. `VARIANT=regional`


### Deploy ###

Two of the scripts are intertwined. This is so that the script that creates Kubernetes Engine clusters (`kubernetes_engine_${VARIANT}_cluster.py`) can provide the cluster's master's endpoint IP to the script that creates the Kubernetes Engine types (`kubernetes_engine_apis.py`). These are joined by a config file:
```
NAME=[[YOUR-DEPOYMENT]]
CLUSTER=[[YOUR-CLUSTER]]
LOCATION=[[YOUR-REGION-OR-ZONE]]

cat generate_apis_${VARIANT}.yaml |\
sed \
  --expression="s|YOUR-CLUSTER-NAME|${CLUSTER}|g" \
  --expression="s|YOUR-CLUSTER-ZONE|${LOCATION}|g" > ./config.tmp.yaml &&
gcloud deployment-manager deployments update ${NAME} \
--project=$PROJECT \
--config=./config.tmp.yaml && \
rm ./config.tmp/yaml
```

This will create a Kubernetes cluster (${NAME}) and 3 distinct types:
```
kubernetes-v1
kubernetes-v1beta1-apps
kubernetes-v1beta1-extensions
```

Then you can create a Deployment and Service on the cluster with, e.g.:
```
gcloud deployment-manager deployments create k \
--template=deployment_deployment.py \
--project=${PROJECT} \
--properties=\
name:henry,\
image:nginx,\
port:80\
```

**NB**: you may replace `name` with any name of your choosing. You may replace `image` with any image that's accessible to your deployment (dockerhub and [GCR](https://cloud.google.com/container-registry/) are good sources). If you do revise the `image`, ensure you specify the correct `port` that the image publishes.

Alternatively, you may create a Deployment, Service and an Ingress.

**NB**: Creating an Ingress will provision an HTTP/S (L7) Load-Balancer for you that will expose your deployment to the public internet.

```
gcloud deployment-manager deployments create k \
--template=kubernetes_deployment_ingress.py \
--project=${PROJECT} \
--properties=\
name:henry,\
image:dazwilkin/simplehttpd@sha256:3b52f4c1ab525df59f5f48f56a2735770f4383ed94b772363357ec16d68c6726,\
port:8080
```


### Tidy Up ###

Delete the cluster either directly or using Deployment Manager:
```
gcloud deployment-manager deployments delete ${NAME} \
--project=${PROJECT}
```

NB While you can delete the Kubernetes deployment, this only deletes the Kubernetes Service and does not (for some reason) delete the Kubernetes Deployment.