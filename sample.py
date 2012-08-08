import yaml
import json
import pystache

with open('request.yml', 'r') as f:
    docs = yaml.load(f.read())

def build_curl(method, path, query, body):
    curl_base = '$ curl -X {0} -H "Content-Type: application/json"'.format(method)
    curl_base = '{0} https://nexus.api.globusonline.org{1}'.format(curl_base,
            path)
    if query is not None:
        query_string = '&'.join(['{0}={1}'.format(key, value) for key, value in
            query.items()])
        curl_base = '{0}?{1}'.format(curl_base, query_string)
    if body is not None:
        curl_base = curl_base + " -d '{0}'".format(json.dumps(body, indent=4))
    return '\t' + curl_base.replace('\n', '\n\t\t')

resources = []
for resource_file in docs['resources']:
    with open(resource_file, 'r') as f:
        resource = yaml.load(f.read())
        for action in resource['actions']:
            action['method'] = action['method'].upper()
            for message in action['messages']:
                body = message['body'] if 'body' in message else None
                query = message['query'] if 'query' in message else None
                path = message['path'] if 'path' in message else action['path']
                message['curl'] = build_curl(action['method'].upper(), path, query, body)

        resources.append(resource)
docs['resources'] = resources
with open('api.restdown', 'w') as f:
    renderer = pystache.renderer.Renderer(escape=lambda u: u)
    with open('restdoc.mustache') as template:
        f.write(renderer.render(template.read(), docs))

