import unittest
import os
import nsv
from io import StringIO

# Get the directory containing the test samples
SAMPLES_DIR = os.path.join(os.path.dirname(__file__), 'samples')

class TestLoad(unittest.TestCase):
    def test_basic_load_file(self):
        """Test loading basic NSV data from file"""
        file_path = os.path.join(SAMPLES_DIR, 'basic.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        self.assertEqual(rows[1], ["value1", "value2", "value3"])
    
    def test_basic_load_string(self):
        """Test loading basic NSV data from string"""
        file_path = os.path.join(SAMPLES_DIR, 'basic.nsv')
        with open(file_path, 'r') as f:
            data = f.read()
        
        rows = nsv.loads(data)
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        self.assertEqual(rows[1], ["value1", "value2", "value3"])
    
    def test_empty_field(self):
        """Test handling of empty fields with backslash token"""
        file_path = os.path.join(SAMPLES_DIR, 'empty_fields.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "", "field3"])
        self.assertEqual(rows[1], ["value1", "", "value3"])
    
    def test_empty_sequence(self):
        """Test handling of empty sequences (double newlines)"""
        file_path = os.path.join(SAMPLES_DIR, 'empty_sequence.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        
        self.assertEqual(len(rows), 3)
        self.assertEqual(rows[0], ["field1", "field2"])
        self.assertEqual(rows[1], [])  # Empty sequence
        self.assertEqual(rows[2], ["value1", "value2"])
    
    def test_comments_in_header(self):
        """Test that comments in header are ignored"""
        file_path = os.path.join(SAMPLES_DIR, 'comments.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2"])
        self.assertEqual(rows[1], ["value1", "value2"])
    
    def test_missing_version(self):
        """Test that missing version raises error"""
        file_path = os.path.join(SAMPLES_DIR, 'missing_version.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)
    
    def test_missing_separator(self):
        """Test that missing separator raises error"""
        file_path = os.path.join(SAMPLES_DIR, 'missing_separator.nsv')
        with open(file_path, 'r') as f:
            with self.assertRaises(ValueError):
                nsv.load(f)

    def test_various_metadata(self):
        """Test handling of various metadata"""
        file_path = os.path.join(SAMPLES_DIR, 'metadata.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        
        self.assertEqual(len(rows), 2)
        
        # Ensure metadata was captured but not interpreted
        with open(file_path, 'r') as f:
            reader = nsv.Reader(f)
            self.assertEqual(reader.metadata["version"], "1.0")
            self.assertEqual(reader.metadata["something"], "value")
            self.assertEqual(reader.metadata["another"], "thing")


class TestDump(unittest.TestCase):
    def test_basic_dump(self):
        """Test dumping basic NSV data"""
        rows = [
            ["field1", "field2", "field3"],
            ["value1", "value2", "value3"]
        ]
        
        # Test dumps (to string)
        nsv_string = nsv.dumps(rows)
        parsed_rows = nsv.loads(nsv_string)
        self.assertEqual(parsed_rows, rows)
        
        # Test dump (to file)
        output_path = os.path.join(SAMPLES_DIR, 'output_basic.nsv')
        with open(output_path, 'w') as f:
            nsv.dump(rows, f)
        
        with open(output_path, 'r') as f:
            loaded_rows = nsv.load(f)
        
        self.assertEqual(loaded_rows, rows)
    
    def test_empty_field_dump(self):
        """Test dumping data with empty fields"""
        rows = [
            ["field1", "", "field3"],
            ["value1", "value2", ""]
        ]
        
        nsv_string = nsv.dumps(rows)
        parsed_rows = nsv.loads(nsv_string)
        self.assertEqual(parsed_rows, rows)
    
    def test_metadata_dump(self):
        """Test dumping with metadata"""
        rows = [
            ["field1", "field2"],
            ["value1", "value2"]
        ]
        
        metadata = {
            "custom": "value",
            "another": "thing"
        }
        
        nsv_string = nsv.dumps(rows, metadata=metadata)
        
        # Parse it back and check metadata
        reader = nsv.Reader(StringIO(nsv_string))
        self.assertEqual(reader.metadata["version"], "1.0")  # Default version
        self.assertEqual(reader.metadata["custom"], "value")
        self.assertEqual(reader.metadata["another"], "thing")
        
        # Check rows too
        parsed_rows = nsv.loads(nsv_string)
        self.assertEqual(parsed_rows, rows)
    
    def test_custom_version_dump(self):
        """Test dumping with custom version"""
        rows = [["field1", "field2"]]
        
        metadata = {"version": "1.0"}  # Explicitly set version
        
        nsv_string = nsv.dumps(rows, metadata=metadata)
        
        reader = nsv.Reader(StringIO(nsv_string))
        self.assertEqual(reader.metadata["version"], "1.0")


class TestEdgeCases(unittest.TestCase):
    def test_empty_data(self):
        """Test handling of empty data"""
        rows = []
        
        nsv_string = nsv.dumps(rows)
        parsed_rows = nsv.loads(nsv_string)
        
        self.assertEqual(len(parsed_rows), 0)
    
    def test_long_strings(self):
        """Test handling of long string values"""
        long_string = "x" * 10000
        rows = [
            ["normal", long_string],
            [long_string, "normal"]
        ]
        
        nsv_string = nsv.dumps(rows)
        parsed_rows = nsv.loads(nsv_string)
        
        self.assertEqual(len(parsed_rows), 2)
        self.assertEqual(parsed_rows[0][1], long_string)
        self.assertEqual(parsed_rows[1][0], long_string)
    
    def test_special_characters(self):
        """Test handling of special characters in field values"""
        file_path = os.path.join(SAMPLES_DIR, 'special_chars.nsv')
        with open(file_path, 'r') as f:
            rows = nsv.load(f)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field with spaces", "field,with,commas", "field\twith\ttabs"])
        self.assertEqual(rows[1], ["field\"with\"quotes", "field'with'quotes", "field\\with\\backslashes"])
    
    def test_numeric_values(self):
        """Test handling of numeric values"""
        rows = [
            [1, 2, 3],
            [4.5, 6.7, 8.9]
        ]
        
        nsv_string = nsv.dumps(rows)
        parsed_rows = nsv.loads(nsv_string)
        
        # Note: We expect strings back since NSV is text-based
        self.assertEqual(parsed_rows[0], ["1", "2", "3"])
        self.assertEqual(parsed_rows[1], ["4.5", "6.7", "8.9"])


if __name__ == '__main__':
    unittest.main()
