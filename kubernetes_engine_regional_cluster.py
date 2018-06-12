def GenerateConfig(context):
  """Generate YAML resource configuration."""

  cluster_name = context.properties['CLUSTER_NAME']
  cluster_region = context.properties['CLUSTER_ZONE']
  number_of_nodes = context.properties['NUM_NODES']

  resources = []
  outputs = []

  resources.append({
      'name': cluster_name,
      'type': 'gcp-types/container-v1beta1:projects.locations.clusters',
      'properties': {
          'parent': 'projects/{}/locations/{}'.format(context.env['project'], cluster_region),
          'cluster': {
              'name': cluster_name,
              'nodePools': [{
                  'name': 'core',
                  'initialNodeCount': number_of_nodes,
                  'config': {
                      'imageType': 'COS',
                      'preemptible': True,
                      'oauthScopes': [
                          'https://www.googleapis.com/auth/' + scope
                          for scope in [
                              'compute',
                              'devstorage.read_only',
                              'logging.write',
                              'monitoring'
                          ]
                      ]
                  },
                  'autoscaling': {
                      'enabled': False
                  },
                  'management': {
                      'autoUpgrade': True,
                      'autoRepair': True,
                      'upgradeOptions': {}
                  }
              }]
          }
      }
  })
  outputs.append({
        'name': 'endpoint',
        'value': '$(ref.' + cluster_name + '.endpoint)'
  })
  return {'resources': resources, 'outputs': outputs}
