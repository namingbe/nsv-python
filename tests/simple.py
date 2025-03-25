META_SEPARATOR = '\n---\n'


def simple_loads(s):
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
            data[-1].append(cell)
    return metadata, data

def simple_dumps(metadata, data):
    header = '\n'.join(metadata)
    body = '\n\n'.join('\n'.join(row) for row in data)
    return f'{header}{META_SEPARATOR}{body}'
