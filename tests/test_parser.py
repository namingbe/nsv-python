import unittest
from io import StringIO
from nsv.parser import reader, DictReader

class TestParser(unittest.TestCase):
    def test_basic_parsing(self):
        data = """v:1.0
---
field1
field2
field3

value1
value2
value3
"""
        file_obj = StringIO(data)
        r = reader(file_obj)
        rows = list(r)
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ["field1", "field2", "field3"])
        
    def test_empty_field(self):
        data = """v:1.0
---
field1
\\
field3

value1
value2
\\
"""
        file_obj = StringIO(data)
        r = reader(file_obj)
        rows = list(r)
        
        self.assertEqual(len(rows), 1)
        self.assertEqual(rows[0], ["field1", "", "field3"])
        
    def test_dict_reader(self):
        data = """v:1.0
cols:id,name,value
---
1
John
100

2
Jane
200
"""
        file_obj = StringIO(data)
        dr = DictReader(file_obj)
        rows = list(dr)
        
        self.assertEqual(len(rows), 2)
        self.assertEqual(rows[0]["id"], "1")
        self.assertEqual(rows[0]["name"], "John")
        self.assertEqual(rows[1]["name"], "Jane")

if __name__ == '__main__':
    unittest.main()
