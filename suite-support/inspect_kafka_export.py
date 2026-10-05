"""Check an actual ArchVerity full JSON export against one Kafka lab recipe."""
import argparse
import json
from pathlib import Path
from prepare_kafka_case import CASES

def check(snapshot, case):
    findings = snapshot.get('findings', [])
    nodes = snapshot.get('nodes', [])
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
    if case['serializer'] == 'explicit' and 'AFG-KAFKA-010' in rule_ids:
        raise ValueError('Independently precise static wire binding was lost')
    return {'status':'KAFKA_EXPORT_CASE_PASS','case':case['id'],'findings':len(findings),'boundary':'Actual export content; the operator must record IDE/build/project identity separately'}

if __name__ == '__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--case',choices=[case['name'] for case in CASES],required=True)
    parser.add_argument('--snapshot',type=Path,required=True)
    args=parser.parse_args()
    try:
        case=next(case for case in CASES if case['name']==args.case)
        print(json.dumps(check(json.loads(args.snapshot.read_text(encoding='utf-8')),case)))
    except ValueError as error:
        parser.error(str(error))
