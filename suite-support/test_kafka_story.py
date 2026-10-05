"""Negative controls for false proof from the actual retained Kafka recordings."""
import copy
import unittest

from inspect_kafka_story import ROOT, check_story, load_story


class KafkaStoryProofTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.native = load_story(ROOT / 'docs/evidence/kafka-3.0.4')

    def setUp(self):
        self.story = copy.deepcopy(self.native)

    def test_native_full_story_including_recovery_passes(self):
        self.assertEqual('KAFKA_STORY_PASS', check_story(self.story)['status'])

    def test_screenshot_metadata_cannot_replace_an_analysis_export(self):
        self.story['k11-proven-drift.json'] = {'target': 'IDEA', 'image': 'screen.png', 'size': [1400, 950]}
        with self.assertRaisesRegex(ValueError, 'Analysis identity/scope/model'):
            check_story(self.story)

    def test_zero_findings_without_the_repaired_dto_is_not_compatibility_proof(self):
        for mutation in ('remove_shapes', 'remove_tenant'):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(self.native)
                repaired = changed['k12-repaired.json']
                if mutation == 'remove_shapes':
                    repaired.pop('dtoShapes')
                else:
                    shape = next(shape for shape in repaired['dtoShapes'] if shape['canonicalName'] == 'demo.producer.Event')
                    shape['fields'] = [field for field in shape['fields'] if field['wireName'] != 'tenant']
                with self.assertRaisesRegex(ValueError, 'shapes are missing|fields do not match'):
                    check_story(changed)

    def test_separate_topics_cannot_hide_a_cross_cluster_edge(self):
        snapshot = self.story['k03-separate.json']
        consumer = next(node for node in snapshot['nodes'] if node['kind'] == 'KAFKA_CONSUMER')
        producer_topic = next(node for node in snapshot['nodes'] if node['kind'] == 'KAFKA_TOPIC' and node['attributes']['clusterScope'] == 'east')
        link = next(edge for edge in snapshot['edges'] if edge['kind'] == 'CONSUMES')
        link.update(fromId=producer_topic['id'], toId=consumer['id'])
        with self.assertRaisesRegex(ValueError, 'edge crosses cluster scope'):
            check_story(self.story)

    def test_wrong_profiles_or_stale_recovery_fingerprint_are_rejected(self):
        for mutation in ('profiles', 'recovery'):
            with self.subTest(mutation=mutation):
                changed = copy.deepcopy(self.native)
                if mutation == 'profiles':
                    changed['k02-shared-unknown.json']['analysisContext']['selectedProfiles'] = ['green']
                else:
                    changed['k01-recovery.json']['analysisContext']['fingerprint'] = changed['k03-separate.json']['analysisContext']['fingerprint']
                with self.assertRaisesRegex(ValueError, 'profile provenance|Recovery did not restore'):
                    check_story(changed)


if __name__ == '__main__':
    unittest.main()
