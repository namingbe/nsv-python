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

def dump(elems, file_obj, metadata=None):
    """Write elements to an NSV file."""
    w = Writer(file_obj, '1.0', metadata)
    w.write_elems(elems)

def dumps(elems, metadata=None):
    """Write elements to an NSV string."""
    output = StringIO()
    dump(elems, output, metadata)
    return output.getvalue()
