#pip install pandas openpyxl

import pandas as pd

# Read an Excel file into a DataFrame
df = pd.read_excel("your_file.xlsx", sheet_name="Sheet1")  # Specify sheet_name if needed
print(df)

# Write a DataFrame to an Excel file
df.to_excel("output_file.xlsx", sheet_name="Sheet1", index=False)  # Set index=False to avoid saving row indices



from openpyxl import load_workbook

# Load an existing workbook
workbook = load_workbook("your_file.xlsx")
sheet = workbook["Sheet1"]  # Access the specific sheet

# Write data to specific cells
sheet["A1"] = "New Value"
sheet.cell(row=2, column=1).value = "Another Value"

# Save the workbook after changes
workbook.save("your_modified_file.xlsx")



from openpyxl import Workbook

# Create a new workbook and select the active sheet
workbook = Workbook()
sheet = workbook.active
sheet.title = "NewSheet"

# Write data to cells
sheet["A1"] = "Header"
sheet["A2"] = "Data"

# Save the new workbook
workbook.save("new_file.xlsx")
