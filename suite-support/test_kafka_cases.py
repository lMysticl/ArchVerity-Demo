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
