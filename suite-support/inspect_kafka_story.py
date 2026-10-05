"""Verify the six retained native exports of the Kafka walkthrough, not a broker."""
import argparse
import json
from pathlib import Path

from inspect_export import unique_keys
from inspect_kafka_export import check as check_case
from prepare_kafka_case import CASES

ROOT = Path(__file__).resolve().parents[1]
STATES = {
    'k01-unknown.json': 'unknown-cluster-and-override',
    'k02-shared-unknown.json': 'shared-cluster-unresolved-serializer',
    'k11-proven-drift.json': 'proven-drift-control',
    'k12-repaired.json': 'compatible-static-control',
    'k03-separate.json': 'separate-clusters-same-topic',
    'k01-recovery.json': 'unknown-cluster-and-override',
}
PROFILE_SOURCES = {
    f'{module}/src/main/resources/application{suffix}.yml'
    for module, profile in [('producer', 'blue'), ('consumer', 'green')]
    for suffix in ['', '-' + profile]
}
RECOVERY_FIELDS = ('projectId', 'projectName', 'runStatus', 'partial',
                   'scopeFingerprint', 'analysisContext', 'coverage', 'nodes',
                   'edges', 'findings', 'dtoShapes', 'diagnostics')


def load_story(directory):
    return {name: json.loads((directory / name).read_text(encoding='utf-8'),
                             object_pairs_hook=unique_keys) for name in STATES}


def check_story(snapshots):
    if set(snapshots) != set(STATES):
        raise ValueError('The six named story checkpoints are required')
    results = []
    for name, case_name in STATES.items():
        snapshot = snapshots[name]
        case = next(item for item in CASES if item['name'] == case_name)
        result = check_case(snapshot, case, 'kafka-profile-lab')
        context = snapshot['analysisContext']
        if context.get('selectedProfiles') != ['default'] or set(context.get('propertySources', [])) != PROFILE_SOURCES:
            raise ValueError('Module profile provenance changed in the recorded story')
        services = [node for node in snapshot['nodes'] if node['kind'] == 'SERVICE']
        identities = {(node.get('serviceId'), node['attributes'].get('repository'),
                       node['attributes'].get('module')) for node in services}
        expected = {(module, f'demo/{module}-repository',
                     f'archverity-kafka-profile-lab.{module}.main')
                    for module in ('producer', 'consumer')}
        if len(services) != 2 or identities != expected:
            raise ValueError('Producer/consumer repository or module identity changed')
        shapes = snapshot.get('dtoShapes')
        if not isinstance(shapes, list) or any(not isinstance(shape, dict) for shape in shapes):
            raise ValueError('Native DTO shapes are missing')
        for module in ('producer', 'consumer'):
            selected = [shape for shape in shapes if shape.get('canonicalName') == f'demo.{module}.Event']
            if len(selected) != 1 or selected[0].get('confidence') != 'RESOLVED' or selected[0].get('opaqueSerialization') is not False:
                raise ValueError('Native Event shape is missing or unresolved')
            fields = selected[0].get('fields')
            expected_names = {'id', 'tenant'} if module == 'consumer' or name == 'k12-repaired.json' else {'id'}
            if not isinstance(fields, list) or any(not isinstance(field, dict) for field in fields):
                raise ValueError('Native Event fields are missing')
            if len(fields) != len(expected_names) or {field.get('wireName') for field in fields} != expected_names:
                raise ValueError('Event fields do not match this story checkpoint')
            if any(field.get('wireType') != 'java.lang.String' or field.get('required') is not True
                   or field.get('nullable') is not False or field.get('ignored') is not False for field in fields):
                raise ValueError('Required Event wire field contract changed')
        topics = [node for node in snapshot['nodes'] if node['kind'] == 'KAFKA_TOPIC']
        if any(node.get('name') != 'orders.events' for node in topics):
            raise ValueError('The recorded topic identity changed')
        scopes = {node['attributes'].get('clusterScope') for node in topics}
        if case['cluster'] == 'shared' and scopes != {'declared-demo'}:
            raise ValueError('The shared declared cluster scope changed')
        if case['cluster'] == 'separate' and scopes != {'east', 'west'}:
            raise ValueError('The separate cluster scopes changed')
        if case['cluster'] == 'unknown' and (len(scopes) != 2 or any(not isinstance(scope, str) or not scope.startswith('unresolved:') for scope in scopes)):
            raise ValueError('Unknown scopes were merged or silently resolved')
        # Topic count alone can hide an edge that wrongly connects the other cluster.
        for kind, relation, module in [('KAFKA_PRODUCER', 'PUBLISHES', 'producer'),
                                       ('KAFKA_CONSUMER', 'CONSUMES', 'consumer')]:
            endpoints = [node for node in snapshot['nodes'] if node['kind'] == kind]
            if len(endpoints) != 1 or endpoints[0].get('serviceId') != module:
                raise ValueError('Kafka endpoint ownership changed')
            endpoint = endpoints[0]
            links = [edge for edge in snapshot['edges'] if edge.get('kind') == relation]
            matching = [topic for topic in topics if topic['attributes']['clusterScope'] == endpoint['attributes'].get('clusterScope')]
            if len(links) != 1 or len(matching) != 1:
                raise ValueError('Kafka endpoint must have one topic in its own scope')
            expected_link = (endpoint['id'], matching[0]['id']) if module == 'producer' else (matching[0]['id'], endpoint['id'])
            if (links[0].get('fromId'), links[0].get('toId')) != expected_link:
                raise ValueError('A Kafka graph edge crosses cluster scope')
        if name == 'k12-repaired.json' and snapshot['findings']:
            raise ValueError('The repaired walkthrough must retain its zero-finding result')
        results.append({'snapshot': name, **result})
    initial, recovery = snapshots['k01-unknown.json'], snapshots['k01-recovery.json']
    if any(initial.get(field) != recovery.get(field) for field in RECOVERY_FIELDS):
        raise ValueError('Recovery did not restore the original model and analysis context')
    drift, repaired = snapshots['k11-proven-drift.json'], snapshots['k12-repaired.json']
    if drift['analysisContext'] != repaired['analysisContext'] or drift['scopeFingerprint'] != repaired['scopeFingerprint']:
        raise ValueError('DTO repair unexpectedly changed the configuration scope')
    return {'status': 'KAFKA_STORY_PASS', 'checkpoints': results,
            'recovery': 'Original model, DTO shapes and configuration context restored',
            'boundary': 'Retained native static exports; no Kafka delivery or deployed configuration proof'}


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--directory', type=Path, default=ROOT / 'docs/evidence/kafka-3.0.4')
    args = parser.parse_args()
    try:
        print(json.dumps(check_story(load_story(args.directory))))
    except (ValueError, OSError) as error:
        parser.error(str(error))
