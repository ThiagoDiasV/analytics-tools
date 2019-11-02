import re
import os
import xlsxwriter
from time import asctime
import csv
from app import app
from tools import delete_previous_workbooks, delete_temp_data


def read_csv(file: str) -> tuple:
    """
    Read csv file and returns a tuple with the csv data.
    """
    with open(file, newline='') as csv_file:
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


def creates_workbook() -> xlsxwriter.Workbook:
    """
    Creates a xlsxwriter.Workbook object and returns it.
    """
    delete_previous_workbooks()
    date = asctime().replace(':', '').replace(' ', '')
    workbook = xlsxwriter.Workbook(
        f'{app.config["WORKSHEETS_FOLDER"]}/{date}.xlsx'
        )

    return workbook


def creates_new_worksheet(
    workbook: xlsxwriter.Workbook,
    filename: str,
    wavelength_range: list,
    abs_values: list
    ) -> xlsxwriter.Workbook.worksheet_class:
    """
    Creates a new worksheet inside the workbook object.
    """
    workbook.add_worksheet(f'{filename}'[:30])
    
