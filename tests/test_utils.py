import os
import nsv
from io import StringIO

SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')
SAMPLES_DATA = {
    'basic': [["field1", "field2", "field3"], ["value1", "value2", "value3"]],
    'empty_fields': [["field1", "", "field3"], ["value1", "", "value3"]],
    'empty_sequence': [["field1", "field2"], [], ["value1", "value2"]],
    'empty_sequence_end': [["field1", "field2"], ["value1", "value2"], []],
    'comments': [["field1", "field2"], ["value1", "value2"]],
    'special_chars': [["field with spaces", "field,with,commas", "field\twith\ttabs"],
                      ["field\"with\"quotes", "field'with'quotes", "field\\with\\backslashes"]],
}


def dump_then_load(data):
    return nsv.loads(nsv.dumps(data))


def load_then_dump(s):
    return nsv.dumps(nsv.loads(s))


def load_sample(name):
    file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
    with open(file_path, 'r') as f:
        rows = nsv.load(f)
    return rows


def loads_sample(name):
    file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
    with open(file_path, 'r') as f:
        _, rows = nsv.loads(f.read())
    return rows