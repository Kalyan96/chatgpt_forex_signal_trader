import xlwings as xw
import time

def update_excel_cell(cell, value, file_path='C:\\Users\\Kalyan\\Downloads\\pyxl_testbook.xlsx'):
    # Connect to an existing workbook
    wb = xw.Book(file_path)
    # Select the sheet
    sheet = wb.sheets['Sheet1']
    # Update the cell value
    sheet.range(cell).value = value

while 1:
    update_excel_cell('A1', time.strftime('%m%d%H%M%S', time.gmtime()))
    update_excel_cell('A2',time.strftime('%m.%d %H.%M.%S', time.gmtime()))
    time.sleep(1)

