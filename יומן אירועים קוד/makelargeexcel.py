import openpyxl
from openpyxl import Workbook
import random

# Function to generate the data
def generate_data(num_rows):
    areas = {"hasharon": "10", "beer sheva": "11", "shaham": "12"}
    data = []

    for i in range(num_rows):
        area = list(areas.keys())[i % len(areas)]
        date = 14
        time = 830 + (i % 50) * 15
        kav = f'{(i % 30) + 1:03}'
        makatkav = f'{areas[area]}{(i % 30) + 1:03}'
        direction = 1 if i % 2 == 0 else 2

        data.append([area, date, time, kav, makatkav, direction])

    return data

# Generate 100,000 rows of data
data = generate_data(100000)

# Create a new Excel workbook and select the active worksheet
wb = Workbook()
ws = wb.active

# Add headers to the worksheet
headers = ["area", "date", "time", "kav", "makatkav", "direction"]
ws.append(headers)

# Append data to the worksheet
for row in data:
    ws.append(row)

# Save the workbook to a file
wb.save("large_dataset.xlsx")

print("100,000 rows have been written to 'large_dataset.xlsx'.")
