# Registry of dialects
_dialects = {}

# Default dialect
class Dialect:
    def __init__(self, empty_token="\\", **kwargs):
        self.empty_token = empty_token
        # Add more dialect options as needed
        for key, value in kwargs.items():
            setattr(self, key, value)

def register_dialect(name, dialect=None, **kwargs):
    """Register a dialect for use with the nsv format."""
    if dialect is None:
        dialect = Dialect(**kwargs)
    _dialects[name] = dialect

def get_dialect(name):
    """Get the dialect registered under the given name."""
    if name not in _dialects:
        if name == 'default':
            # Register default dialect
            register_dialect('default')
        else:
            raise ValueError(f"Unknown dialect: {name}")
    return _dialects[name]

def list_dialects():
    """Return a list of all registered dialect names."""
    return list(_dialects.keys())

# Register default dialect
register_dialect('default')
