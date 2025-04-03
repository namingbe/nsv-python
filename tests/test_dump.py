import unittest
import tempfile
import os
import nsv
from io import StringIO
from test_utils import SAMPLES_DATA, dump_then_load

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
                s = f.read()
                loaded_rows = nsv.loads(s)
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
        self.assertEqual(['v:1.0'] + metadata, reader.metadata)

        parsed_rows = nsv.loads(nsv_string)
        self.assertEqual(parsed_rows, rows)


if __name__ == '__main__':
    unittest.main()