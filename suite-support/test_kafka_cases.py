import copy
import json
import subprocess
import tempfile
import unittest
from pathlib import Path
from prepare_kafka_case import CASES, LAB, prepare_case
from inspect_kafka_export import check

def complete_snapshot():
    return {'schemaVersion':1,'projectId':'kafka-demo','runStatus':'COMPLETE','partial':False,
            'analysisContext':{'fingerprint':'kafka-test-context'},'coverage':{},'edges':[]}


def add_pattern_operations(snapshot):
    """Synthetic validator control, not an observation of plugin execution."""
    listener = {'path':'consumer/src/main/java/demo/consumer/Listener.java','symbol':'receive'}
    bindings = 'consumer/src/main/java/demo/consumer/KafkaBindings.java'
    consumer = {'id':'pattern-consumer','kind':'KAFKA_CONSUMER','name':'receive',
                'attributes':{'topicPattern':r'orders\..*','wireConfidence':'INFERRED'},
                'sources':[listener],
                'evidence':[
                    {'label':'Consumer topic declaration','value':r'orders\..*','source':listener,'confidence':'RESOLVED'},
                    {'label':'Kafka bean listener_factory','value':'listenerFactory -> consumerFactory',
                     'source':{'path':bindings,'symbol':'listenerFactory'},'confidence':'RESOLVED'},
                    {'label':'Kafka bean consumer_factory',
                     'value':'consumerFactory -> org.springframework.kafka.support.serializer.JsonDeserializer',
                     'source':{'path':bindings,'symbol':'consumerFactory'},'confidence':'RESOLVED'}],
                'kafkaWireContract':{'bindingConfidence':'RESOLVED',
                    'keySerde':{'className':'org.apache.kafka.common.serialization.StringDeserializer','settingsComplete':True},
                    'valueSerde':{'className':'org.springframework.kafka.support.serializer.JsonDeserializer','settingsComplete':True}}}
    producer = {'id':'literal-producer','kind':'KAFKA_PRODUCER','name':'publish',
                'attributes':{'wireConfidence':'RESOLVED'},
                'kafkaWireContract':{'bindingConfidence':'RESOLVED',
                    'keySerde':{'className':'org.apache.kafka.common.serialization.StringSerializer','settingsComplete':True},
                    'valueSerde':{'className':'org.springframework.kafka.support.serializer.JsonSerializer','settingsComplete':True}}}
    snapshot['nodes'].extend([consumer,producer])
    for finding in snapshot['findings']:
        if finding['ruleId']=='AFG-KAFKA-010':
            finding.update(subjectId=consumer['id'],sources=[listener])


class KafkaCasesTest(unittest.TestCase):
    def test_each_case_is_clean_isolated_and_baseline_is_unchanged(self):
        baseline={str(path.relative_to(LAB)):path.read_bytes() for path in LAB.rglob('*') if path.is_file() and not any(part in {'.gradle','build'} for part in path.parts)}
        with tempfile.TemporaryDirectory() as folder:
            for case in CASES:
                result=prepare_case(case['name'],Path(folder)/case['id'])
                root=Path(result['project'])
                self.assertEqual('',subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True))
                self.assertEqual(case,result['case'])
                self.assertIn('include: blue',(root/'producer/src/main/resources/application.yml').read_text())
                self.assertIn('include: green',(root/'consumer/src/main/resources/application.yml').read_text())
                if case['cluster']=='separate':
                    self.assertIn('cluster: east',(root/'producer/src/main/resources/application-blue.yml').read_text())
                    self.assertIn('cluster: west',(root/'consumer/src/main/resources/application-green.yml').read_text())
            with self.assertRaisesRegex(ValueError,'overwrite'):
                prepare_case(CASES[0]['name'],Path(folder)/CASES[0]['id'])
        self.assertEqual(baseline,{str(path.relative_to(LAB)):path.read_bytes() for path in LAB.rglob('*') if path.is_file() and not any(part in {'.gradle','build'} for part in path.parts)})

    def test_validator_rejects_the_original_false_pass_and_lost_provenance(self):
        case=CASES[0]
        snapshot={'nodes':[{'kind':'KAFKA_TOPIC','attributes':{'clusterConfidence':'INFERRED'},'evidence':[{'label':'Configuration','source':{'path':f'{module}/src/main/resources/application-{profile}.yml'}}]} for module,profile in [('producer','blue'),('consumer','green')]],
                  'findings':[{'ruleId':rule,'disposition':'UNKNOWN','evidence':[{'label':"Unresolved configuration override 'KAFKA_VALUE_SERIALIZER'"}]} for rule in case['expected']]}
        snapshot.update(complete_snapshot())
        self.assertEqual('KAFKA_EXPORT_CASE_PASS',check(snapshot,case)['status'])
        for mutate in (lambda value:value['nodes'].pop(),lambda value:value['nodes'][0].update(evidence=[]),
                       lambda value:value['findings'].append({'ruleId':'AFG-KAFKA-005','disposition':'PROVEN_MISMATCH'}),
                       lambda value:value['nodes'][0]['attributes'].update(clusterConfidence='RESOLVED'),
                       lambda value:value['findings'][0].update(disposition='OBSERVATION'),
                       lambda value:value['findings'].append({'ruleId':'AFG-KAFKA-005','disposition':'UNKNOWN'}),
                       lambda value:[item.update(evidence=[]) for item in value['findings']]):
            candidate=copy.deepcopy(snapshot)
            mutate(candidate)
            with self.assertRaises(ValueError):check(candidate,case)

    def test_each_recipe_accepts_its_full_contract_and_rejects_partial_or_wrong_target(self):
        for case in CASES:
            with self.subTest(case=case['id']):
                snapshot=complete_snapshot()
                profile_evidence=[{'label':'Configuration','source':{'path':f'{module}/src/main/resources/application-{profile}.yml'}}
                                  for module,profile in [('producer','blue'),('consumer','green')]]
                if case['unresolved']:
                    profile_evidence.append({'label':"Unresolved configuration override 'KAFKA_VALUE_SERIALIZER'"})
                snapshot['nodes']=[{'kind':'KAFKA_TOPIC','attributes':{'clusterConfidence':'INFERRED' if case['cluster']=='unknown' else 'EXACT'},
                                    'evidence':profile_evidence} for _ in range(1 if case['cluster']=='shared' else 2)]
                snapshot['findings']=[{'ruleId':rule,'disposition':'PROVEN_MISMATCH' if rule=='AFG-KAFKA-005' and case['proven'] else 'UNKNOWN'}
                                       for rule in case['expected']]
                if case['pattern']:
                    add_pattern_operations(snapshot)
                self.assertEqual('KAFKA_EXPORT_CASE_PASS',check(snapshot,case,'kafka-demo')['status'])
                for patch in ({'runStatus':'PARTIAL'},{'partial':True},{'runStatus':'FAILED'},
                              {'runStatus':'CANCELLED'},{'projectId':'other'},{'analysisContext':{}},
                              {'schemaVersion':2}):
                    bad=copy.deepcopy(snapshot)
                    bad.update(patch)
                    with self.subTest(patch=patch),self.assertRaises(ValueError):check(bad,case,'kafka-demo')
                if case['expected']:
                    snapshot['findings'].pop()
                    with self.assertRaisesRegex(ValueError,'Missing expected'):check(snapshot,case)

    def test_pattern_unknown_is_bound_to_the_consumer_and_preserves_resolved_factories(self):
        for case in (case for case in CASES if case['pattern']):
            snapshot=complete_snapshot()
            profile_evidence=[{'label':'Configuration','source':{'path':f'{module}/src/main/resources/application-{profile}.yml'}}
                              for module,profile in [('producer','blue'),('consumer','green')]]
            snapshot['nodes']=[{'kind':'KAFKA_TOPIC',
                                'attributes':{'clusterConfidence':'INFERRED' if case['cluster']=='unknown' else 'EXACT'},
                                'evidence':profile_evidence} for _ in range(2)]
            snapshot['findings']=[{'ruleId':rule,'disposition':'UNKNOWN'} for rule in case['expected']]
            add_pattern_operations(snapshot)
            self.assertEqual('KAFKA_EXPORT_CASE_PASS',check(snapshot,case)['status'])
            # Operations are the last two nodes in this deliberately small control.
            mutations=[
                ('missing 010',lambda s:s['findings'].__setitem__(slice(None),[f for f in s['findings'] if f['ruleId']!='AFG-KAFKA-010'])),
                ('wrong subject',lambda s:s['findings'][-1].update(subjectId='adjacent-consumer')),
                ('producer 010',lambda s:s['findings'].append({'ruleId':'AFG-KAFKA-010','disposition':'UNKNOWN','subjectId':'literal-producer'})),
                ('proven consumer wire',lambda s:s['nodes'][-2]['attributes'].update(wireConfidence='RESOLVED')),
                ('inferred producer wire',lambda s:s['nodes'][-1]['attributes'].update(wireConfidence='INFERRED')),
                ('empty pattern',lambda s:s['nodes'][-2]['attributes'].update(topicPattern='')),
                ('duplicate consumer',lambda s:s['nodes'].append(copy.deepcopy(s['nodes'][-2]))),
                ('duplicate producer',lambda s:s['nodes'].append(copy.deepcopy(s['nodes'][-1]))),
                ('wrong listener source',lambda s:s['nodes'][-2]['sources'][0].update(path='consumer/Other.java')),
                ('wrong finding source',lambda s:s['findings'][-1].update(sources=[{'path':'consumer/Other.java','symbol':'receive'}])),
                ('malformed finding source',lambda s:s['findings'][-1].update(sources=[{'path':[],'symbol':'receive'}])),
                ('lost listener factory',lambda s:s['nodes'][-2]['evidence'].pop(1)),
                ('lost consumer factory',lambda s:s['nodes'][-2]['evidence'].pop(2)),
                ('unresolved factory evidence',lambda s:s['nodes'][-2]['evidence'][1].update(confidence='INFERRED')),
                ('wrong factory source',lambda s:s['nodes'][-2]['evidence'][2]['source'].update(path='producer/KafkaBindings.java')),
                ('lost pattern provenance',lambda s:s['nodes'][-2]['evidence'].pop(0)),
                ('invented cross-scope DTO',lambda s:s['findings'].append({'ruleId':'AFG-KAFKA-005','disposition':'UNKNOWN'})),
            ]
            for offset in (-2,-1):
                mutations.append((f'unresolved binding {offset}',lambda s,o=offset:s['nodes'][o]['kafkaWireContract'].update(bindingConfidence='INFERRED')))
                for key in ('keySerde','valueSerde'):
                    mutations.append((f'wrong serde {offset}/{key}',lambda s,o=offset,k=key:s['nodes'][o]['kafkaWireContract'][k].update(className='example.CustomSerde')))
                    mutations.append((f'incomplete settings {offset}/{key}',lambda s,o=offset,k=key:s['nodes'][o]['kafkaWireContract'][k].update(settingsComplete=False)))
            for name,mutate in mutations:
                candidate=copy.deepcopy(snapshot)
                mutate(candidate)
                with self.subTest(case=case['id'],mutation=name),self.assertRaises(ValueError):
                    check(candidate,case)

    def test_explicit_nonpattern_cases_still_reject_any_wire_unknown(self):
        for case in (case for case in CASES if case['serializer']=='explicit' and not case['pattern']):
            snapshot=complete_snapshot()
            evidence=[{'label':'Configuration','source':{'path':f'{module}/src/main/resources/application-{profile}.yml'}}
                      for module,profile in [('producer','blue'),('consumer','green')]]
            snapshot['nodes']=[{'kind':'KAFKA_TOPIC','attributes':{'clusterConfidence':'RESOLVED'},'evidence':evidence}
                               for _ in range(1 if case['cluster']=='shared' else 2)]
            snapshot['findings']=[{'ruleId':rule,'disposition':'PROVEN_MISMATCH' if case['proven'] else 'UNKNOWN'}
                                   for rule in case['expected']]
            self.assertEqual('KAFKA_EXPORT_CASE_PASS',check(snapshot,case)['status'])
            snapshot['findings'].append({'ruleId':'AFG-KAFKA-010','disposition':'UNKNOWN'})
            with self.subTest(case=case['id']),self.assertRaisesRegex(ValueError,'Independently precise'):
                check(snapshot,case)

    def test_malformed_nested_evidence_is_rejected_with_a_recoverable_error(self):
        case=CASES[10]
        valid=complete_snapshot()
        valid['nodes']=[{'kind':'KAFKA_TOPIC','attributes':{},'evidence':[
            {'label':'Configuration','source':{'path':f'{module}/src/main/resources/application-{profile}.yml'}}
            for module,profile in [('producer','blue'),('consumer','green')]]}]
        valid['findings']=[{'ruleId':'AFG-KAFKA-005','disposition':'PROVEN_MISMATCH'}]
        self.assertEqual('KAFKA_EXPORT_CASE_PASS',check(valid,case)['status'])
        for patch in ({'attributes':[]},{'evidence':None},{'evidence':[None]},
                      {'evidence':[{'label':None}]},{'evidence':[{'source':'bad'}]},
                      {'evidence':[{'source':{'path':[]}}]}):
            bad=copy.deepcopy(valid)
            bad['nodes'][0].update(patch)
            with self.subTest(patch=patch),self.assertRaises(ValueError):check(bad,case)

if __name__=='__main__':unittest.main()
