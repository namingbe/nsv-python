class writer:
    def __init__(self, file_obj, dialect='default', **kwargs):
        self.file_obj = file_obj
        from .dialects import get_dialect
        self.dialect = get_dialect(dialect)
        self.metadata = {"v": "1.0"}
        self.header_written = False
        
    def writeheader(self, **metadata):
        # Update metadata with provided values
        self.metadata.update(metadata)
        
        # Write metadata
        for key, value in self.metadata.items():
            if key == "v":
                self.file_obj.write(f"v:{value}\n")
            else:
                self.file_obj.write(f"{key}:{value}\n")
                
        # Write separator
        self.file_obj.write("---\n")
        self.header_written = True
        
    def writerow(self, row):
        if not self.header_written:
            self.writeheader()
            
        # Replace empty strings with empty field token
        escaped_row = ["\\" if field == "" else str(field) for field in row]
        self.file_obj.write("\n".join(escaped_row))
        self.file_obj.write("\n\n")  # Row separator
        
    def writerows(self, rows):
        for row in rows:
            self.writerow(row)


class DictWriter:
    def __init__(self, file_obj, fieldnames, dialect='default', **kwargs):
        self.writer = writer(file_obj, dialect, **kwargs)
        self.fieldnames = fieldnames
        
    def writeheader(self, **metadata):
        metadata["cols"] = ",".join(self.fieldnames)
        self.writer.writeheader(**metadata)
        
    def writerow(self, row_dict):
        row = [row_dict.get(field, "") for field in self.fieldnames]
        self.writer.writerow(row)
        
    def writerows(self, row_dicts):
        for row_dict in row_dicts:
            self.writerow(row_dict)
