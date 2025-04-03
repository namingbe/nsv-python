import unittest
import os
import tempfile
import nsv
from io import StringIO
from test_utils import SAMPLES_DIR, SAMPLES_DATA

class TestMultilineAndTrailingNewlines(unittest.TestCase):
    def test_multiline_encoded(self):
        """Test reading data with encoded newlines."""
        file_path = os.path.join(SAMPLES_DIR, 'multiline_encoded.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual([["line1\nline2", "field2", "field3"], ["anotherline1\nline2\nline3", "value2", "value3"]], rows)

        # Test round-trip works correctly
        output = StringIO()
        nsv.dump(rows, output)
        output.seek(0)
        round_trip_rows = nsv.load(output)
        self.assertEqual(rows, round_trip_rows)

    def test_trailing_newline(self):
        """Test file with trailing newline."""
        file_path = os.path.join(SAMPLES_DIR, 'trailing_newline.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['basic'] + [[]], rows)

    def test_no_trailing_newline(self):
        """Test file without trailing newline."""
        file_path = os.path.join(SAMPLES_DIR, 'no_trailing_newline.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['basic'], rows)

    def test_multiline_roundtrip(self):
        """Test writing and reading data with encoded newlines."""
        data = [
            ["line1\nline2", "field2"],
            ["value1", "value2\nvalue2continued"]
        ]

        with tempfile.TemporaryDirectory() as output_dir:
            file_path = os.path.join(output_dir, 'multiline_test.nsv')
            with open(file_path, 'w') as f:
                nsv.dump(data, f)
            with open(file_path, 'r') as f:
                rows = nsv.load(f)
            self.assertEqual(data, rows)

            with open(file_path, 'r') as f:
                content = f.read()
                self.assertIn("line1\\nline2", content)
                self.assertIn("value2\\nvalue2continued", content)


if __name__ == '__main__':
    unittest.main()