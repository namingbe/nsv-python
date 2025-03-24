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

# Reading NSV data
with open('input.nsv', 'r') as f:
    reader = nsv.load(f)
    for row in reader:
        print(row)

# Writing NSV data
with open('output.nsv', 'w') as f:
    writer = nsv.Writer(f)
    writer.write_elem(['field1', 'field2', 'field3'])
    writer.write_elem(['value1', 'value2', 'value3'])
```

## Running Tests

```bash
cd tests
python -m unittest
```
