import xlrd
import collections
import json
import re
import time
import subprocess
import sys
import os


try:
    import pyexcel
    print(f"{pyexcel.__name__} sucessfully imported")
except:
    print(f"Need to install pyexcel")
    subprocess.call([sys.executable, "-m", "pip", "install", "--user", 'pyexcel'])
    subprocess.call([sys.executable, "-m", "pip", "install", "--user", 'pyexcel-xlsx'])



def add_to_records(single_record, list_of_details):
    """Append record of a single order to list of records """
    print("\nFn: \"add_to_records\" ")
    try:
        list_of_details.append(single_record)
        print("record added")
        print("\nCurrent record added")
        print(json.dumps(single_record, indent=2))
        print("\n")

        print(list_of_details)
    except:
        print("record not added")
    return list_of_details


def excel_to_list(fname):
    result_list = []

    xl_workbook = xlrd.open_workbook(fname)
    xl_sheet = xl_workbook.sheet_by_index(0)

    for row_idx in range(1, xl_sheet.nrows):
        value1 = str(xl_sheet.cell(rowx=row_idx, colx=0).value)
        value2 = str(xl_sheet.cell(rowx=row_idx, colx=1).value)
        value3 = str(xl_sheet.cell(rowx=row_idx, colx=2).value)

        current_record = collections.OrderedDict()

        port_regex = re.compile(r"(\d{5}).")
        port = port_regex.search(value2).group(1).strip()

        current_record['proxy_id'] = value3
        current_record['proxy_address'] = value1
        current_record['port'] = port

        add_to_records(current_record, result_list)

    print(result_list)
    return result_list


def excel_single_item_list(fname):
    result_list = []

    xl_workbook = xlrd.open_workbook(fname)
    xl_sheet = xl_workbook.sheet_by_index(0)

    for row_idx in range(1, xl_sheet.nrows):
        value1 = str(xl_sheet.cell(rowx=row_idx, colx=0).value)
        value2 = str(xl_sheet.cell(rowx=row_idx, colx=1).value)
        value3 = str(xl_sheet.cell(rowx=row_idx, colx=2).value)

        current_record = collections.OrderedDict()

        port_regex = re.compile(r"(\d{5}).")
        port = port_regex.search(value2).group(1).strip()

        current_record['value'] = value3

        add_to_records(current_record, result_list)

    print(result_list)
    return result_list


def listOfJSONtoExcel(jsonList, fullDestfilename):
    print("Saving results")
    search_results_name = "AmazonOrdersPlaced"
    time_run = time.strftime("%Y%b%d_%H%M%S", time.localtime())
    dest_file_name = f"C:/saveToFile/{fullDestfilename}_{time_run}.xlsx"

    try:
        pyexcel.save_as(records=jsonList, dest_file_name=dest_file_name)
        print(f"Results saved at: {dest_file_name}")
    except:
        print("Save directory not present. Making directory")
        os.makedirs('C:/saveToFile/' + search_results_name)
        try:
            pyexcel.save_as(records=jsonList, dest_file_name=dest_file_name)
            print(f"Results saved at: {dest_file_name}")
            print("\n")
        except:
            print("Save failed")


