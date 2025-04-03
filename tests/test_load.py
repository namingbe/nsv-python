import unittest
import os
import nsv
from test_utils import SAMPLES_DIR, SAMPLES_DATA, load_sample, loads_sample


class TestLoad(unittest.TestCase):
    def test_load(self):
        for name, data in SAMPLES_DATA.items():
            rows = load_sample(name)
            self.assertEqual(data, rows, msg=name)

    def test_loads(self):
        for name, data in SAMPLES_DATA.items():
            rows = loads_sample(name)
            self.assertEqual(data, rows, msg=name)

    def test_basic_load_file(self):
        """Test loading basic NSV data from file."""
        file_path = os.path.join(SAMPLES_DIR, 'basic.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['basic'], rows)

    def test_basic_load_string(self):
        """Test loading basic NSV data from string."""
        file_path = os.path.join(SAMPLES_DIR, 'basic.nsv')
        with open(file_path, 'r') as f:
            data = f.read()
        rows = nsv.loads(data)

        self.assertEqual(SAMPLES_DATA['basic'], rows)

    def test_empty_field(self):
        """Test handling of empty fields with backslash token."""
        file_path = os.path.join(SAMPLES_DIR, 'empty_fields.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['empty_fields'], rows)

    def test_empty_sequence(self):
        """Test handling of empty sequences (double newlines)."""
        file_path = os.path.join(SAMPLES_DIR, 'empty_sequence.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['empty_sequence'], rows)

    def test_comments_in_header(self):
        """Test that comments in header are ignored."""
        file_path = os.path.join(SAMPLES_DIR, 'comments.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['comments'], rows)

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


if __name__ == '__main__':
    unittest.main()