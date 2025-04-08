import os
import unittest

from test_utils import SAMPLES_DATA, dump_sample, dumps_sample, SAMPLES_DIR


class TestDump(unittest.TestCase):
    def test_dump(self):
        for name in SAMPLES_DATA:
            actual = dump_sample(name)
            file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
            with open(file_path, 'r') as f:
                expected = f.read()
            self.assertEqual(expected, actual, msg=name)

    def test_dumps(self):
        for name, data in SAMPLES_DATA.items():
            actual = dumps_sample(name)
            file_path = os.path.join(SAMPLES_DIR, f'{name}.nsv')
            with open(file_path, 'r') as f:
                expected = f.read()
            self.assertEqual(expected, actual, msg=name)


if __name__ == '__main__':
    unittest.main()
