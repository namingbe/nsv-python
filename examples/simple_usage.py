"""
Simple example showing basic usage of the NSV package.
"""
import nsv
import io

# Example data
data = """v:1.0
table:3
cols:id,name,value
---
1
John Doe
100

2
Jane Smith
200

3
Bob Johnson
150
"""

# Reading NSV
file_obj = io.StringIO(data)
reader = nsv.DictReader(file_obj)

print("Reading NSV data:")
for row in reader:
    print(f"ID: {row['id']}, Name: {row['name']}, Value: {row['value']}")

# Writing NSV
output = io.StringIO()
writer = nsv.DictWriter(output, fieldnames=['id', 'name', 'value'])
writer.writeheader(table=3)  # Specify additional metadata

# Write some rows
writer.writerows([
    {'id': '1', 'name': 'John Doe', 'value': '100'},
    {'id': '2', 'name': 'Jane Smith', 'value': '200'},
    {'id': '3', 'name': 'Bob Johnson', 'value': '150'}
])

# Display the result
output.seek(0)
print("\nGenerated NSV data:")
print(output.read())

# CSV conversion example
import csv
csv_data = io.StringIO()
csv_writer = csv.writer(csv_data)
csv_writer.writerow(['id', 'name', 'age'])
csv_writer.writerow(['101', 'Alice', '25'])
csv_writer.writerow(['102', 'Bob', '30'])

csv_data.seek(0)
nsv_data = nsv.from_csv(csv_data)

print("\nConverted from CSV to NSV:")
print(nsv_data.read())
