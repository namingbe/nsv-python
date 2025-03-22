import unittest
from io import StringIO
from nsv.writer import writer, DictWriter
from nsv.parser import reader

class TestWriter(unittest.TestCase):
    def test_basic_writing(self):
        file_obj = StringIO()
        w = writer(file_obj)
        w.writerow(["field1", "field2", "field3"])
        w.writerow(["value1", "value2", "value3"])
        
        # Reset position to read
        file_obj.seek(0)
        
        r = reader(file_obj)
        rows = list(r)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        self.assertEqual(rows[1], ["value1", "value2", "value3"])
        
    def test_empty_field_writing(self):
        file_obj = StringIO()
        w = writer(file_obj)
        w.writerow(["field1", "", "field3"])
        
        # Reset position to read
        file_obj.seek(0)
        
        r = reader(file_obj)
        rows = list(r)
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ["field1", "", "field3"])
        
    def test_dict_writer(self):
        file_obj = StringIO()
        fieldnames = ["id", "name", "value"]
        dw = DictWriter(file_obj, fieldnames)
        dw.writeheader()
        dw.writerow({"id": 1, "name": "John", "value": 100})
        dw.writerow({"id": 2, "name": "Jane", "value": 200})
        
        # Reset position to read
        file_obj.seek(0)
        
        from nsv.parser import DictReader
        dr = DictReader(file_obj)
        rows = list(dr)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], "1")
        self.assertEqual(rows[0]["name"], "John")
        self.assertEqual(rows[1]["name"], "Jane")

if __name__ == '__main__':
    unittest.main()
