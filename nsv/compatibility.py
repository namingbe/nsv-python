import csv
from io import StringIO

def from_csv(csv_file, dialect='excel', **kwargs):
    """Convert CSV data to NSV format."""
    csv_reader = csv.reader(csv_file, dialect=dialect, **kwargs)
    nsv_data = StringIO()
    
    from .writer import writer
    nsv_writer = writer(nsv_data)
    
    # Write the header
    nsv_writer.writeheader()
    
    # Write the rows
    nsv_writer.writerows(csv_reader)
    
    # Reset the StringIO position
    nsv_data.seek(0)
    return nsv_data

def to_csv(nsv_file, dialect='excel', **kwargs):
    """Convert NSV data to CSV format."""
    from .parser import reader
    nsv_reader = reader(nsv_file)
    
    csv_data = StringIO()
    csv_writer = csv.writer(csv_data, dialect=dialect, **kwargs)
    
    # Write the rows
    for row in nsv_reader:
        csv_writer.writerow(row)
    
    # Reset the StringIO position
    csv_data.seek(0)
    return csv_data
