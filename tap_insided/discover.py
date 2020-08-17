import os
import json

from singer.catalog import Catalog, CatalogEntry, Schema

from tap_insided.endpoints import ENDPOINTS_CONFIG

SCHEMAS = {}
FIELD_METADATA = {}

def get_endpoints(endpoints=None):
    if not endpoints:
        endpoints = ENDPOINTS_CONFIG

    for stream_name, endpoint in endpoints.items():
        yield stream_name, endpoint

        if 'children' in endpoint:
            yield from get_endpoints(endpoint['children'])

def get_abs_path(path):
    return os.path.join(os.path.dirname(os.path.realpath(__file__)), path)

def get_schema(stream_name, endpoint):
    global SCHEMAS, FIELD_METADATA

    if stream_name in SCHEMAS:
        return SCHEMAS[stream_name], FIELD_METADATA[stream_name]

    schemas_path = get_abs_path('schemas')

    filename = endpoint.get('schema_filename')
    if not filename:
        filename = '{}.json'.format(stream_name)

    with open(os.path.join(schemas_path, filename)) as data_file:
        schema = json.load(data_file)

    metadata = []
    for prop, json_schema in schema['properties'].items():
        if prop in endpoint['pk']:
            inclusion = 'automatic'
        else:
            inclusion = 'available'
        metadata.append({
            'metadata': {
                'inclusion': inclusion
            },
            'breadcrumb': ['properties', prop]
        })

    SCHEMAS[stream_name] = schema
    FIELD_METADATA[stream_name] = metadata

    return schema, metadata

def discover():
    catalog = Catalog([])

    for stream_name, endpoint_config in get_endpoints():
        schema_dict, metadata = get_schema(stream_name, endpoint_config)
        schema = Schema.from_dict(schema_dict)

        catalog.streams.append(CatalogEntry(
            stream=stream_name,
            tap_stream_id=stream_name,
            key_properties=endpoint_config['pk'],
            schema=schema,
            metadata=metadata
        ))

    return catalog
