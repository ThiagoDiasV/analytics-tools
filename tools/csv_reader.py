import xlsxwriter
from time import asctime
import csv
from app import app
from tools import delete_previous_workbooks, delete_temp_data
from scipy.signal import savgol_filter


def read_csv(file: str) -> list:
    """
    Read csv file and returns a list with the csv data.
    """
    try:
        with open(file, newline='', encoding='utf-8') as csv_file:
            data = list(csv.reader(csv_file, delimiter=';'))
    except UnicodeDecodeError:
        with open(file, newline='', encoding='latin-1') as csv_file:
            data = list(csv.reader(csv_file, delimiter=';'))
    return data


def get_filename(data: list) -> str:
    """
    Get the filename of csv object.
    """
    # This slicing below is to strip the '.csv' of the filename
    filename = data[0][0][:-4]
    return filename


def get_wavelength_range(data: list) -> list:
    """
    Get the wavelength range of values.
    """
    # The real data is after position 2 of the tuple
    # which explains this slicing.
    data = list(data)[2:]

    wavelength_range = sorted((
        lambda_value[0] for lambda_value in data
    ))
    return wavelength_range


def get_absorbance_values(data: list) -> list:
    """
    Get the absorbance values.
    """
    data = list(data)[2:]
    abs_values = [
        abs_value[1] for abs_value in data
    ]
    return abs_values


def applies_savgol_filter(
    data: list, window_length: int, polyorder: int
    ) -> list:
    """
    Applies Saviztky-Golay filter to absorbances.
    """
    data = [
        value.replace(',', '.') for value in data
    ]
    savgol_values = savgol_filter(data, window_length, polyorder)
    return savgol_values


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


def custom_map(function, sequence):
    """
    Applies a custom map function to a sequence.
    """
    return [
        function(item) for item in sequence
    ]


def pipeline(files, filename, windowlength, polyorder):
    csv_data_list = custom_map(read_csv, files)

    filenames = custom_map(get_filename, csv_data_list)

    wavelength_range = get_wavelength_range(csv_data_list[0])

    abs_values_list = custom_map(get_absorbance_values, csv_data_list)

    full_results = {
        k: v for k, v in zip(filenames, abs_values_list)
    }

    savgol_values = custom_map(
        lambda x: applies_savgol_filter(x, windowlength, polyorder),
        abs_values_list
        )

    full_savgol_results = {
        k: v for k, v in zip(filenames, savgol_values)
    }

    workbook = creates_workbook(filename)
    creates_new_worksheet(workbook, filename, wavelength_range, full_results)
    creates_new_worksheet(
        workbook, f'{filename}savgol',
        wavelength_range, full_savgol_results
        )
    closes_workbook(workbook)
    delete_temp_data()
