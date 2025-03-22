from .parser import reader, DictReader
from .writer import writer, DictWriter
from .dialects import register_dialect, get_dialect, list_dialects
from .compatibility import from_csv, to_csv

__version__ = "0.1.0"
