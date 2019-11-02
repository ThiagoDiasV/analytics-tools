import re
import os
import xlsxwriter
from time import asctime
import csv
from app import app
from tools import delete_previous_workbooks, delete_temp_data
from pprint import pprint


def read_csv(file: str) -> tuple:
    """
    Read csv file and returns a tuple with the csv data.
    """
    try:
        with open(file, newline='', encoding='utf-8') as csv_file:
            data = tuple(csv.reader(csv_file, delimiter=';'))
    except UnicodeDecodeError:
        with open(file, newline='', encoding='latin-1') as csv_file:
            data = tuple(csv.reader(csv_file, delimiter=';'))
    return data


def get_filename(data: tuple) -> str:
    """
    Get the filename of csv object.
    """
    # This slicing below is to strip the '.csv' of the filename
    filename = data[0][0][:-4]
    return filename


def get_wavelength_range(data: tuple) -> list:
    """
    Get the wavelength range of values.
    """
    # The real data is after position 2 of the tuple
    # which explains this slicing.
    data = tuple(data)[2:]

    wavelength_range = sorted((
        lambda_value[0] for lambda_value in data
    ))
    return wavelength_range


def get_absorbance_values(data: tuple) -> list:
    """
    Get the absorbance values.
    """
    data = tuple(data)[2:]
    abs_values = tuple(
        abs_value[1] for abs_value in data
    )
    return abs_values


def creates_workbook(filename) -> xlsxwriter.Workbook:
    """
    Creates a xlsxwriter.Workbook object and returns it.
    """
    delete_previous_workbooks()
    date = asctime().replace(':', '').replace(' ', '')
    workbook = xlsxwriter.Workbook(
        f'{app.config["WORKSHEETS_FOLDER"]}/{filename}{date}.xlsx'
        )

    return workbook


def creates_new_worksheet(
    workbook: xlsxwriter.Workbook,
    filename: str,
    wavelength_range: list,
    full_values: dict
    ) -> xlsxwriter.Workbook.worksheet_class:
    """
    Creates a new worksheet inside the workbook object.
    """
    worksheet = workbook.add_worksheet(f'{filename}')
    worksheet.write(0, 0, 'nm')
    worksheet.write_column(1, 0, wavelength_range)
    row = 0
    col = 1
    for sample, data in full_values.items():
        worksheet.write(row, col, sample)
        worksheet.write_column(row + 1, col, data)
        col += 1


def closes_workbook(workbook):
    workbook.close()


def pipeline(files, filename):
    csv_data_list = [
        read_csv(file) for file in files
    ]

    filenames = [
        get_filename(csv_data) for csv_data in csv_data_list
    ]

    wavelength_range = get_wavelength_range(csv_data_list[0])

    abs_values_list = [
        get_absorbance_values(data) for data in csv_data_list
    ]

    full_results = {
        k: v for k, v in zip(filenames, abs_values_list)
    }

    workbook = creates_workbook(filename)
    creates_new_worksheet(workbook, filename, wavelength_range, full_results)
    closes_workbook(workbook)
    delete_temp_data()
