class reader:
    def __init__(self, file_obj, dialect='default', **kwargs):
        self.file_obj = file_obj
        from .dialects import get_dialect
        self.dialect = get_dialect(dialect)
        # Parse metadata header
        self._parse_header()
        # Apply kwargs to override dialect settings
        
    def _parse_header(self):
        # Read until metadata separator
        header_lines = []
        meta_sep = "\n---\n"
        buffer = ""
        
        # Read until we find the metadata separator
        while True:
            chunk = self.file_obj.read(1024)
            if not chunk:
                raise ValueError("Invalid NSV: No metadata separator found")
            
            buffer += chunk
            if meta_sep in buffer:
                break
                
        # Split at first occurrence of separator
        header_text, remaining = buffer.split(meta_sep, 1)
        
        # Put remaining text back into stream (if possible)
        if hasattr(self.file_obj, "seek"):
            self.file_obj.seek(self.file_obj.tell() - len(remaining))
        else:
            # For non-seekable file objects, we'll need to buffer
            self._buffer = remaining
            
        # Parse metadata lines
        self.metadata = {}
        for line in header_text.split("\n"):
            line = line.strip()
            if not line or line.startswith(("#", "//", "--", "x-")):
                continue
                
            if ":" in line:
                key, value = line.split(":", 1)
                self.metadata[key] = value
            else:
                # Handle special case for version
                if line.startswith("v:"):
                    self.metadata["version"] = line[2:]
        
        # Verify required metadata
        if "version" not in self.metadata:
            raise ValueError("Invalid NSV: Missing version information")
    
    def __iter__(self):
        return self
        
    def __next__(self):
        # Read until double newline
        row_text = self._read_until_double_newline()
        if row_text is None:
            raise StopIteration
            
        # Split on single newlines
        return [field if field != "\\" else "" for field in row_text.split("\n")]
        
    def _read_until_double_newline(self):
        buffer = ""
        
        while True:
            line = self.file_obj.readline()
            if not line:  # EOF
                return buffer if buffer else None
                
            buffer += line
            
            # Check for row boundary (double newline)
            if buffer.endswith("\n\n"):
                return buffer[:-2]  # Remove the double newline


class DictReader:
    def __init__(self, file_obj, fieldnames=None, restkey=None, restval=None, dialect='default', **kwargs):
        self.reader = reader(file_obj, dialect, **kwargs)
        self.fieldnames = fieldnames
        self.restkey = restkey
        self.restval = restval
        
        # If fieldnames aren't provided, try to get them from metadata
        if self.fieldnames is None:
            if "cols" in self.reader.metadata:
                self.fieldnames = self.reader.metadata["cols"].split(",")
            else:
                # Use first row as fieldnames
                try:
                    self.fieldnames = next(self.reader)
                except StopIteration:
                    self.fieldnames = []
    
    def __iter__(self):
        return self
        
    def __next__(self):
        row = next(self.reader)
        
        # Convert to dict similar to csv.DictReader
        d = {}
        for i, value in enumerate(row):
            if i < len(self.fieldnames):
                d[self.fieldnames[i]] = value
            elif self.restkey:
                if self.restkey not in d:
                    d[self.restkey] = []
                d[self.restkey].append(value)
        
        # Add missing fields with restval
        if self.restval is not None:
            for key in self.fieldnames:
                if key not in d:
                    d[key] = self.restval
                    
        return d
