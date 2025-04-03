import unittest
import os
import nsv
from test_utils import SAMPLES_DIR, SAMPLES_DATA

class TestEdgeSequences(unittest.TestCase):
    def test_empty_sequence_start(self):
        """Test handling of empty sequence at start."""
        file_path = os.path.join(SAMPLES_DIR, 'empty_sequence_start.nsv')
        with open(file_path, 'r') as f:
            data = nsv.load(f)

        self.assertEqual([[], ["field1", "field2"], ["value1", "value2"]], data)

    def test_multiple_empty_sequences(self):
        """Test handling of multiple consecutive empty sequences."""
        file_path = os.path.join(SAMPLES_DIR, 'multiple_empty_sequences.nsv')
        with open(file_path, 'r') as f:
            data = nsv.load(f)

        self.assertEqual([[], ["field1", "field2"], [], ["value1", "value2"]], data)

    def test_empty_sequence_end(self):
        """Test handling of empty sequence at end."""
        file_path = os.path.join(SAMPLES_DIR, 'empty_sequence_end.nsv')
        with open(file_path, 'r') as f:
            data = nsv.load(f)

        self.assertEqual(SAMPLES_DATA['empty_sequence_end'], data)

    def test_only_empty_sequences(self):
        """Test file with only empty sequences."""
        file_path = os.path.join(SAMPLES_DIR, 'only_empty_sequences.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)

        self.assertEqual([[], []], rows)

    def test_extra_newline_after_separator(self):
        """Test handling of extra newline after header separator."""
        file_path = os.path.join(SAMPLES_DIR, 'extra_newline_after_separator.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)


if __name__ == '__main__':
    unittest.main()