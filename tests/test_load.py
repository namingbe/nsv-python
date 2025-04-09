import unittest
import os
from csv import excel

import nsv
from test_utils import SAMPLES_DIR, SAMPLES_DATA, load_sample, loads_sample


class TestLoad(unittest.TestCase):
    def test_load(self):
        for name, expected in SAMPLES_DATA.items():
            with self.subTest(sample_name=name):
                actual = load_sample(name)
                self.assertEqual(expected, actual)

    def test_loads(self):
        for name, expected in SAMPLES_DATA.items():
            with self.subTest(sample_name=name):
                actual = loads_sample(name)
                self.assertEqual(expected, actual)

    def test_missing_version(self):
        """Test that missing version raises error."""
        file_path = os.path.join(SAMPLES_DIR, 'missing_version.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)

    def test_missing_separator(self):
        """Test that missing separator raises error."""
        file_path = os.path.join(SAMPLES_DIR, 'missing_separator.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)

    def test_extra_newline_after_separator(self):
        file_path = os.path.join(SAMPLES_DIR, 'extra_newline_after_separator.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)


if __name__ == '__main__':
    unittest.main()
