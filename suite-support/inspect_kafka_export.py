"""Check an actual ArchVerity full JSON export against one Kafka lab recipe."""
import argparse
import json
from pathlib import Path
from prepare_kafka_case import CASES
from inspect_export import validate_analysis, unique_keys

def _source_matches(source, path, symbol):
    return (isinstance(source, dict)
            and isinstance(source.get('path'), str)
            and source.get('path', '').replace('\\', '/') == path
            and source.get('symbol') == symbol)


def _check_explicit_pattern(nodes, findings):
    consumers = [node for node in nodes if node['kind'] == 'KAFKA_CONSUMER']
    producers = [node for node in nodes if node['kind'] == 'KAFKA_PRODUCER']
    if len(consumers) != 1 or len(producers) != 1:
        raise ValueError('Pattern control needs exactly one producer and one consumer')
    consumer, producer = consumers[0], producers[0]
    consumer_id = consumer.get('id')
    producer_id = producer.get('id')
    if (not isinstance(consumer_id, str) or not consumer_id.strip()
            or consumer.get('name') != 'receive' or producer.get('name') != 'publish'
            or not isinstance(producer_id, str) or not producer_id.strip() or producer_id == consumer_id):
        raise ValueError('Pattern control lost its receive/publish operation identity')
    pattern = consumer['attributes'].get('topicPattern')
    if (not isinstance(pattern, str) or not pattern.strip()
            or consumer['attributes'].get('wireConfidence') != 'INFERRED'
            or producer['attributes'].get('wireConfidence') != 'RESOLVED'):
        raise ValueError('Only the pattern consumer may retain inferred wire confidence')
    wire_findings = [finding for finding in findings if finding['ruleId'] == 'AFG-KAFKA-010']
    if (len(wire_findings) != 1 or wire_findings[0].get('disposition') != 'UNKNOWN'
            or wire_findings[0].get('subjectId') != consumer_id):
        raise ValueError('Pattern control needs exactly one consumer 010 UNKNOWN and no producer 010')
    listener_path = 'consumer/src/main/java/demo/consumer/Listener.java'
    for entity in (consumer, wire_findings[0]):
        sources = entity.get('sources', [])
        if (not isinstance(sources, list)
                or not any(_source_matches(source, listener_path, 'receive') for source in sources)):
            raise ValueError('Pattern consumer/finding lost its Listener.java source')
    for node, suffix in ((consumer, 'Deserializer'), (producer, 'Serializer')):
        contract = node.get('kafkaWireContract')
        if not isinstance(contract, dict) or contract.get('bindingConfidence') != 'RESOLVED':
            raise ValueError('Pattern control must retain both resolved factory/serde bindings')
        for key, expected in (('keySerde', 'org.apache.kafka.common.serialization.String' + suffix),
                              ('valueSerde', 'org.springframework.kafka.support.serializer.Json' + suffix)):
            serde = contract.get(key)
            if (not isinstance(serde, dict) or serde.get('className') != expected
                    or serde.get('settingsComplete') is not True):
                raise ValueError('Pattern control lost its exact JSON/default-key serde or complete settings')
    evidence = consumer.get('evidence', [])
    bindings_path = 'consumer/src/main/java/demo/consumer/KafkaBindings.java'
    for label, value, symbol in (
            ('Kafka bean listener_factory', 'listenerFactory -> consumerFactory', 'listenerFactory'),
            ('Kafka bean consumer_factory',
             'consumerFactory -> org.springframework.kafka.support.serializer.JsonDeserializer', 'consumerFactory')):
        if not any(item.get('label') == label and item.get('value') == value
                   and item.get('confidence') == 'RESOLVED'
                   and _source_matches(item.get('source'), bindings_path, symbol) for item in evidence):
            raise ValueError('Pattern control lost resolved listener/consumer factory provenance')
    if not any(item.get('label') == 'Consumer topic declaration' and item.get('value') == pattern
               and item.get('confidence') == 'RESOLVED'
               and _source_matches(item.get('source'), listener_path, 'receive') for item in evidence):
        raise ValueError('Pattern control lost its resolved Listener.java pattern declaration')


def check(snapshot, case, expected_project_id=None):
    validate_analysis(snapshot, require_complete=True, expected_project_id=expected_project_id)
    findings = snapshot.get('findings', [])
    nodes = snapshot.get('nodes', [])
    if any(not isinstance(finding.get('ruleId'),str) or not finding['ruleId'].strip() for finding in findings):
        raise ValueError('Finding rule identity is missing')
    if any(not isinstance(node.get('kind'),str) or not node['kind'].strip() for node in nodes):
        raise ValueError('Node kind is missing')
    for node in nodes:
        if not isinstance(node.get('attributes', {}), dict):
            raise ValueError('Node attributes must be an object')
    for entity in [*nodes, *findings]:
        evidence = entity.get('evidence', [])
        if not isinstance(evidence, list) or any(not isinstance(item, dict) for item in evidence):
            raise ValueError('Evidence must be an array of objects')
        for item in evidence:
            if not isinstance(item.get('label', ''), str):
                raise ValueError('Evidence label must be text')
            source = item.get('source')
            if source is not None and (not isinstance(source, dict) or not isinstance(source.get('path', ''), str)):
                raise ValueError('Evidence source/path is malformed')
    rule_ids = {finding['ruleId'] for finding in findings}
    missing = set(case['expected']) - rule_ids
    if missing:
        raise ValueError(f'Missing expected findings: {sorted(missing)}')
    if any(finding.get('disposition') != 'UNKNOWN' for finding in findings if finding['ruleId'] in {'AFG-KAFKA-009','AFG-KAFKA-010'}):
        raise ValueError('Unresolved scope or wire binding must remain an explicit UNKNOWN')
    proven = [finding for finding in findings if finding['ruleId'] == 'AFG-KAFKA-005' and finding.get('disposition') == 'PROVEN_MISMATCH']
    if bool(proven) != case['proven']:
        raise ValueError('Wire compatibility/drift was asserted outside the case proof boundary')
    contract_findings = [finding for finding in findings if finding['ruleId'] == 'AFG-KAFKA-005']
    if contract_findings and (case['cluster'] != 'shared' or case['dto'] == 'equal'):
        raise ValueError('A DTO contract was invented across distinct scopes or for equal DTO shapes')
    if 'AFG-KAFKA-005' in case['expected']:
        expected_disposition = 'PROVEN_MISMATCH' if case['proven'] else 'UNKNOWN'
        if any(finding.get('disposition') != expected_disposition for finding in contract_findings):
            raise ValueError('The DTO finding lost its required proof disposition')
    topics = [node for node in nodes if node['kind'] == 'KAFKA_TOPIC']
    expected_topics = 1 if case['cluster'] == 'shared' else 2
    if len(topics) != expected_topics:
        raise ValueError(f'Topic scopes must remain distinct: expected {expected_topics}, got {len(topics)}')
    evidence = [item for node in nodes for item in node.get('evidence', [])] + [item for finding in findings for item in finding.get('evidence', [])]
    paths = {item.get('source', {}).get('path', '').replace('\\', '/') for item in evidence if item.get('source')}
    for required in ('producer/src/main/resources/application-blue.yml','consumer/src/main/resources/application-green.yml'):
        if not any(path.endswith(required) for path in paths):
            raise ValueError(f'Missing profile provenance: {required}')
    unresolved = any(item.get('label','').startswith('Unresolved configuration') for item in evidence)
    if unresolved != case['unresolved']:
        raise ValueError('External/cyclic override uncertainty was dropped or incorrectly retained')
    if case['cluster'] == 'unknown' and any(topic.get('attributes', {}).get('clusterConfidence') in {'EXACT','RESOLVED'} for topic in topics):
        raise ValueError('An unknown cluster was silently promoted')
    if case['cluster'] != 'unknown' and 'AFG-KAFKA-009' in rule_ids:
        raise ValueError('Declared logical cluster failed to resolve')
    if case['serializer'] == 'explicit':
        if case['pattern']:
            _check_explicit_pattern(nodes, findings)
        elif 'AFG-KAFKA-010' in rule_ids:
            raise ValueError('Independently precise static wire binding was lost')
    return {'status':'KAFKA_EXPORT_CASE_PASS','case':case['id'],'findings':len(findings),
            'projectId':snapshot['projectId'],'analysisContext':snapshot['analysisContext']['fingerprint'],
            'boundary':'Complete export content; the operator must record IDE/build/project identity separately'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=[case['name'] for case in CASES],required=True)
    parser.add_argument('--snapshot',type=Path,required=True)
    parser.add_argument('--project-id',help='Exact projectId observed in this case export')
    args=parser.parse_args()
    try:
        case=next(case for case in CASES if case['name']==args.case)
        print(json.dumps(check(json.loads(args.snapshot.read_text(encoding='utf-8'),object_pairs_hook=unique_keys),case,args.project_id)))
    except (ValueError, OSError) as error:
        parser.error(str(error))
