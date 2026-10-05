"""Prepare one isolated, clean Kafka profile case; never change the shipped lab."""
import argparse
import json
import subprocess
from pathlib import Path
from prepare_project import ROOT, prepare

LAB = ROOT / 'projects/kafka-profile-lab'
CASES = json.loads((LAB / 'cases.json').read_text(encoding='utf-8'))
SERIALIZER = 'org.springframework.kafka.support.serializer.JsonSerializer'

def prepare_case(name, destination):
    case = next((item for item in CASES if item['name'] == name), None)
    if case is None:
        raise ValueError(f'Unknown Kafka case: {name}')
    result = prepare('kafka-profile-lab', destination)
    root = Path(result['project'])
    def change(relative, before, after):
        path = root / relative
        text = path.read_text(encoding='utf-8')
        if text.count(before) != 1:
            raise ValueError(f'Fixture drift: {name}: {relative}')
        path.write_text(text.replace(before, after, 1), encoding='utf-8', newline='\n')
    config = root / '.archflow.yml'
    if case['cluster'] == 'shared':
        config.write_text(config.read_text(encoding='utf-8') + 'kafka:\n  defaultCluster: declared-demo\n', encoding='utf-8', newline='\n')
    elif case['cluster'] == 'separate':
        for module, profile, cluster in (('producer','blue','east'),('consumer','green','west')):
            path = root / f'{module}/src/main/resources/application-{profile}.yml'
            path.write_text(path.read_text(encoding='utf-8') + f'archflow:\n  kafka:\n    cluster: {cluster}\n', encoding='utf-8', newline='\n')
    producer_config = 'producer/src/main/resources/application-blue.yml'
    placeholder = '${KAFKA_VALUE_SERIALIZER}'
    mode = case['serializer']
    if mode == 'explicit':
        change(producer_config, placeholder, SERIALIZER)
        change('producer/src/main/java/demo/producer/KafkaBindings.java',
               'new DefaultKafkaProducerFactory<>(Map.of("value.serializer", configuredSerializer))',
               'new DefaultKafkaProducerFactory<>(Map.of(), new StringSerializer(), new JsonSerializer<>())')
    elif mode in {'nested', 'cycle'}:
        change(producer_config, placeholder, '${wire.serializer}')
        path = root / producer_config
        value = placeholder if mode == 'nested' else '${spring.kafka.producer.value-serializer}'
        path.write_text(path.read_text(encoding='utf-8') + f'wire:\n  serializer: {value}\n', encoding='utf-8', newline='\n')
    elif mode == 'fallback':
        change(producer_config, placeholder, '${KAFKA_VALUE_SERIALIZER:' + SERIALIZER + '}')
    elif mode == 'override':
        change('.archflow.yml', '  profiles: [default]', f'  profiles: [default]\n  propertyOverrides:\n    KAFKA_VALUE_SERIALIZER: {SERIALIZER}')
    if case['dto'] == 'equal':
        change('consumer/src/main/java/demo/consumer/Event.java', ', @JsonProperty(required = true) String tenant', '')
    if case['pattern']:
        change('consumer/src/main/java/demo/consumer/Listener.java', 'topics = "${topics.orders}"', 'topicPattern = "orders\\\\..*"')
    subprocess.run(['git','add','--all'],cwd=root,check=True,capture_output=True)
    subprocess.run(['git','-c','user.name=ArchVerity Demo Fixture','-c','user.email=demo@invalid.example',
                    'commit','--quiet','--allow-empty','-m',f"Kafka case {case['id']}: {name}"],cwd=root,check=True,capture_output=True)
    result['case'] = case
    result['baseline'] = subprocess.check_output(['git','rev-parse','HEAD'],cwd=root,text=True).strip()
    if subprocess.check_output(['git','status','--porcelain'],cwd=root,text=True).strip():
        raise AssertionError('Prepared Kafka case must be clean')
    return result

if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', choices=[case['name'] for case in CASES], required=True)
    parser.add_argument('--output', type=Path, required=True)
    args = parser.parse_args()
    try:
        print(json.dumps(prepare_case(args.case, args.output)))
    except ValueError as error:
        parser.error(str(error))
