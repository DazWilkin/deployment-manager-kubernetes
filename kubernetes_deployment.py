def GenerateConfig(context):
  """Generate YAML resource configuration."""

  cluster_types_root = '{}/kubernetes'.format(context.env['project'])
  cluster_types = {
      'Service': '{}-v1:/api/v1/namespaces/{{namespace}}/services'.format(cluster_types_root),
      'Deployment': '{}-v1beta1-apps:/apis/apps/v1beta1/namespaces/{{namespace}}/deployments'.format(cluster_types_root)
  }

  name = context.properties['name']
  image = context.properties['image']
  port = context.properties['port']

  resources = [{
      'name': 'deployment',
      'type': cluster_types['Deployment'],
      'properties': {
          'apiVersion': 'apps/v1beta1',
          'kind': 'Deployment',
          'namespace': 'default',
          'metadata': {
              'name': name
          },
          'spec': {
              'replicas': 1,
              'template': {
                  'metadata': {
                      'labels': {
                          'name': name
                      }
                  },
                  'spec': {
                      'containers': [{
                          'name': 'container',
                          'image': image,
                          'ports': [{
                              'containerPort': port
                          }]
                      }]
                  }
              }
          }
      }
  }, {
      'name': 'service',
      'type': cluster_types['Service'],
      'properties': {
          'apiVersion': 'v1',
          'kind': 'Service',
          'namespace': 'default',
          'metadata': {
              'name': name,
              'labels': {
                  'id': 'deployment-manager'
              }
          },
          'spec': {
              'type': 'NodePort',
              'ports': [{
                  'port': port,
                  'targetPort': port,
                  'protocol': 'TCP'
              }],
              'selector': {
                  'name': name
              }
          }
      }
  }]

  return {'resources': resources}