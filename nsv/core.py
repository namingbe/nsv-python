from .reader import Reader
from .writer import Writer

def load(file_obj):
    """Load NSV data from a file-like object."""
    r = Reader(file_obj)
    return r.metadata, list(r)

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
    if body:
        for row in body.split('\n\n'):
            acc = []
            for cell in row.split('\n'):
                if cell:  # split can leave a trailing empty one
                    acc.append(Reader.unescape(cell))
            data.append(acc)
    return metadata, data

def dump(data, file_obj, metadata=None):
    """Write elements to an NSV file."""
    w = Writer(file_obj, metadata)
    w.write_rows(data)
    return file_obj

def dumps(data, metadata=None):
    """Write elements to an NSV string."""
    header = '\n'.join(metadata or ('v:1.0',))
    body = '\n\n'.join('\n'.join(map(Writer.escape, row)) for row in data)
    return f'{header}{META_SEPARATOR}{body}\n'

# todo: do properly, make interface clean
def prepare_metadata(raw=(), version='1.0'):
    return [f'v:{version}'] + raw

META_SEPARATOR = '\n---\n'
