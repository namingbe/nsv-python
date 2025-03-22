# NSV Python

Python implementation of the [NSV (Newline-Separated Values)](https://github.com/namingbe/nsv) format.

## Installation

### From PyPI

```bash
pip install nsv
```

### From Source

```bash
git clone https://github.com/namingbe/nsv-python.git
cd nsv-python
pip install -e .
```

## Usage

### Basic Reading and Writing

```python
import nsv
import io

# Reading NSV data
with open('data.nsv', 'r') as f:
    reader = nsv.reader(f)
    for row in reader:
        print(row)  # List of field values

# Writing NSV data
with open('output.nsv', 'w') as f:
    writer = nsv.writer(f)
    writer.writeheader(table=3)  # Specify metadata
    writer.writerow(['field1', 'field2', 'field3'])
    writer.writerow(['value1', 'value2', 'value3'])
```

### Dictionary Interface

```python
import nsv

# Reading with column names
with open('data.nsv', 'r') as f:
    reader = nsv.DictReader(f)
    for row in reader:
        print(row)  # Dictionary mapping column names to values

# Writing with column names
with open('output.nsv', 'w') as f:
    writer = nsv.DictWriter(f, fieldnames=['id', 'name', 'value'])
    writer.writeheader(table=3)
    writer.writerow({'id': '1', 'name': 'John', 'value': '100'})
```

### CSV Conversion

```python
import nsv
import csv
from io import StringIO

# Convert from CSV to NSV
with open('data.csv', 'r') as csv_file:
    nsv_data = nsv.from_csv(csv_file)
    with open('output.nsv', 'w') as nsv_file:
        nsv_file.write(nsv_data.getvalue())

# Convert from NSV to CSV
with open('data.nsv', 'r') as nsv_file:
    csv_data = nsv.to_csv(nsv_file)
    with open('output.csv', 'w') as csv_file:
        csv_file.write(csv_data.getvalue())
```

## Running Tests

```bash
# Run all tests
python -m unittest discover

# Run specific test file
python -m unittest tests.test_parser
python -m unittest tests.test_writer
python -m unittest tests.test_csv_compat
```

