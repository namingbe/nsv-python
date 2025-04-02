from .reader import Reader
from .writer import Writer

def load(file_obj):
    """Load NSV data from a file-like object."""
    r = Reader(file_obj)
    return list(r)

def loads(s):
    """Load NSV data from a string."""
    header, body = s.split(META_SEPARATOR, 1)  # will raise ValueError here if no separator
    version = None
    metadata = []
    for line in header.split('\n'):
        if line == 'v:1.0':
            version = '1.0'
        metadata.append(line)
    if version is None:
        raise ValueError("Invalid NSV: Missing version information")
    data = []
    for row in body.split('\n\n'):
        data.append([])
        for cell in row.split('\n'):
            data[-1].append(Reader.unescape(cell))
    return metadata, data

def dump(data, file_obj, version='1.0', metadata=()):
    """Write elements to an NSV file."""
    w = Writer(file_obj, version, metadata)
    w.write_elems(data)
    return file_obj

def dumps(data, metadata=('v:1.0',)):
    """Write elements to an NSV string."""
    header = '\n'.join(metadata)
    body = '\n\n'.join('\n'.join(map(Writer.escape, row)) for row in data)
    return f'{header}{META_SEPARATOR}{body}'

# todo: do properly, make interface clean
def prepare_metadata(raw=(), version='1.0'):
    return [f'v:{version}'] + raw

META_SEPARATOR = '\n---\n'
