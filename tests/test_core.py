import tempfile
import unittest
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


class TestLoad(unittest.TestCase):
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


class TestDump(unittest.TestCase):
    def test_basic_dump(self):
        """Test dumping basic NSV data."""
        rows = SAMPLES_DATA['basic']

        # Test dumps (to string)
        self.assertEqual(dump_then_load(rows), rows)

        # Test dump (to file)
        with tempfile.TemporaryDirectory() as output_dir:
            output_path = os.path.join(output_dir, 'output_basic.nsv')
            with open(output_path, 'w') as f:
                nsv.dump(rows, f)
            with open(output_path, 'r') as f:
                loaded_rows = nsv.load(f)
            self.assertEqual(loaded_rows, rows)

    def test_empty_field_dump(self):
        """Test dumping data with empty fields."""
        data = SAMPLES_DATA['empty_fields']

        self.assertEqual(data, dump_then_load(data))

    def test_metadata_dump(self):
        """Test dumping with metadata."""
        rows = [
            ["field1", "field2"],
            ["value1", "value2"]
        ]
        metadata = ["something", "something:else"]
        nsv_string = nsv.dumps(rows, metadata=metadata)

        reader = nsv.Reader(StringIO(nsv_string))
        self.assertEqual('1.0', reader.version)
        self.assertEqual(metadata, reader.metadata)

        parsed_rows = nsv.loads(nsv_string)
        self.assertEqual(parsed_rows, rows)


class TestEdgeCases(unittest.TestCase):
    def test_empty_data(self):
        """Test handling of empty data."""
        data = []
        self.assertEqual(data, dump_then_load(data))

    def test_long_strings(self):
        """Test handling of long string values."""
        long_string = ''.join(chr(x) for x in range(11, 50000))
        data = [
            ["normal", long_string],
            [long_string, "normal"]
        ]
        self.assertEqual(data, dump_then_load(data))

    def test_special_characters(self):
        """Test handling of special characters in field values."""
        file_path = os.path.join(SAMPLES_DIR, 'special_chars.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        self.assertEqual(SAMPLES_DATA['special_chars'], rows)

    def test_numeric_values(self):
        """Test handling of numeric values."""
        data = [
            [1, 2, 3],
            [4.5, 6.7, 8.9]
        ]
        actual = dump_then_load(data)

        # Note: We expect strings back since NSV is text-based
        self.assertEqual([["1", "2", "3"], ["4.5", "6.7", "8.9"]], actual)


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


class TestIncrementalProcessing(unittest.TestCase):
    def test_incremental_reading(self):
        """Test reading elements incrementally."""
        file_path = os.path.join(SAMPLES_DIR, 'incremental.nsv')
        with open(file_path, 'r') as f:
            reader = nsv.Reader(f)

            first = next(reader)
            self.assertEqual(first, ["field1", "field2"])

            second = next(reader)
            self.assertEqual(second, ["value1", "value2"])

            third = next(reader)
            self.assertEqual(third, ["last1", "last2"])

            # Should be at end of the file
            with self.assertRaises(StopIteration):
                next(reader)

    def test_incremental_writing(self):
        """Test writing elements incrementally."""
        data = [["field1", "field2"], ["value1", "value2"], ["last1", "last2"]]
        with tempfile.TemporaryDirectory() as output_dir:
            output_path = os.path.join(output_dir, 'output_incremental.nsv')

            with open(output_path, 'w') as f:
                writer = nsv.Writer(f)
                for elem in data:
                    writer.write_elem(elem)

            with open(output_path, 'r') as f:
                actual = nsv.load(f)

            self.assertEqual(data, actual)


if __name__ == '__main__':
    unittest.main()
