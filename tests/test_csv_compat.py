import unittest
import csv
from io import StringIO
from nsv.compatibility import from_csv, to_csv
from nsv.parser import reader

class TestCSVCompatibility(unittest.TestCase):
    def test_from_csv(self):
        # Create CSV data
        csv_data = StringIO()
        csv_writer = csv.writer(csv_data)
        csv_writer.writerow(["field1", "field2", "field3"])
        csv_writer.writerow(["value1", "value2", "value3"])
        
        # Reset position
        csv_data.seek(0)
        
        # Convert to NSV
        nsv_data = from_csv(csv_data)
        
        # Read NSV
        r = reader(nsv_data)
        rows = list(r)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        self.assertEqual(rows[1], ["value1", "value2", "value3"])
        
    def test_to_csv(self):
        # Create NSV data
        nsv_data = StringIO()
        from nsv.writer import writer
        w = writer(nsv_data)
        w.writeheader()
        w.writerow(["field1", "field2", "field3"])
        w.writerow(["value1", "value2", "value3"])
        
        # Reset position
        nsv_data.seek(0)
        
        # Convert to CSV
        csv_data = to_csv(nsv_data)
        
        # Read CSV
        csv_reader = csv.reader(csv_data)
        rows = list(csv_reader)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        self.assertEqual(rows[1], ["value1", "value2", "value3"])

if __name__ == '__main__':
    unittest.main()
