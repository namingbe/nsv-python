from io import StringIO

from .reader import Reader
from .writer import Writer

def load(file_obj):
    """Load NSV data from a file-like object."""
    r = Reader(file_obj)
    return list(r)

def loads(string):
    """Load NSV data from a string."""
    return load(StringIO(string))

def dump(data, file_obj, version='1.0', metadata=()):
    """Write elements to an NSV file."""
    w = Writer(file_obj, version, metadata)
    w.write_elems(data)

def dumps(data, version='1.0', metadata=()):
    """Write elements to an NSV string."""
    output = StringIO()
    dump(data, output, version, metadata)
    return output.getvalue()
