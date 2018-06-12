def GenerateConfig(context):
  """Generate YAML resource configuration."""

  cluster_types_root = '{}/kubernetes'.format(context.env['project'])
  cluster_types = {
      'Service': '{}:/api/v1/namespaces/{{namespace}}/services'.format(cluster_types_root),
      'Deployment': '{}-apps:/apis/apps/v1beta1/namespaces/{{namespace}}/deployments'.format(cluster_types_root)
  }

  name = context.properties['name']
  image = context.properties['image']
  port = context.properties['port']

  resources = [{
      'name': name + '-service',
      'type': cluster_types['Service'],
      'properties': {
          'apiVersion': 'v1',
          'kind': 'Service',
          'namespace': 'default',
          'metadata': {
              'name': name + '-service',
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
                  'app': name
              }
          }
      }
  }, {
      'name': name + '-deployment',
      'type': cluster_types['Deployment'],
      'properties': {
          'apiVersion': 'apps/v1beta1',
          'kind': 'Deployment',
          'namespace': 'default',
          'metadata': {
              'name': name + '-deployment'
          },
          'spec': {
              'replicas': 1,
              'template': {
                  'metadata': {
                      'labels': {
                          'name': name + '-deployment',
                          'app': name
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
  }]

  return {'resources': resources}
