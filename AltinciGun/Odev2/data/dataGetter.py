import pathlib
import openpyxl
import os

def getExcelDataWithSelectedSheet(excelFileName,selectedSheetName):
    path = pathlib.Path(__file__).parent.parent.resolve() #to access test_sauce.py file root path    
    os.chdir(f"{path}\data")
    excelFile = openpyxl.load_workbook(excelFileName)    
    selectedSheet = excelFile[selectedSheetName] 
    return selectedSheet