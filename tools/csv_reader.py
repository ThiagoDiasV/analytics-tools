import xlsxwriter
from time import asctime
import csv
from app import app
from tools import delete_previous_workbooks, delete_temp_data
from scipy.signal import savgol_filter
# from string import ascii_uppercase
from pdb import set_trace


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


def get_real_values_data(data: list) -> list:
    # Get real data values of csv file
    for index, row in enumerate(data):
        if row[0].replace(',', '').replace('-', '').isdigit() and row[1].replace(',', '').replace('-', '').isdigit():
            initial_data_flag = index
            break
    data = list(data)[initial_data_flag:]
    return data


def get_wavelength_range(data: list) -> list:
    """
    Get the wavelength range of values.
    """

    wavelength_range = sorted((
        lambda_value[0] for lambda_value in data
    ))
    return wavelength_range


def get_absorbance_values(data: list) -> list:
    """
    Get the absorbance values.
    """
    abs_values = [
        float(abs_value[1].replace(',', '.')) for abs_value in data
    ]
    return abs_values


def applies_savgol_filter(
        data: list, window_length: int, polyorder: int
        ) -> list:
    """
    Applies Saviztky-Golay filter to absorbances.
    """
    data = [
        float(str(value).replace(',', '.')) for value in data
    ]
    savgol_values = savgol_filter(data, window_length, polyorder)
    return savgol_values


def prepare_data_to_derivate(data: list, wv_range: list,
                             delta_lambda: int) -> list:
    """
    Prepares the data to do derivative spectroscopy calculus
    """
    data = [
        float(str(value).replace(',', '.')) for value in data
    ]

    # This list below will receive the data to do derivative spectroscopy
    values_to_derivative = list()

    # Prepare the data
    for i in range(delta_lambda):
        wv_list = [x for a, x in enumerate(wv_range) if a % delta_lambda == i]
        abs_values = [y for b, y in enumerate(data) if b % delta_lambda == i]
        results = {k: v for k, v in zip(wv_list, abs_values)}
        values_to_derivative.append(results)

    return values_to_derivative


def derivate(data_to_derivate: dict, delta_lambda: int) -> list:
    """
    Function which derivates data using the derivative spectroscopy formula.
    """

    # Wavelength values
    wv_values = list(data_to_derivate.keys())

    # Absorbance values
    abs_values = list(data_to_derivate.values())

    # New dict which will receive the derivative values
    deriv_results = dict()

    # Iteration through the absorbances
    # calculating derivative spectroscopy values.
    for index, value in enumerate(abs_values):
        if index == 0:
            deriv_results[wv_values[index]] = (
                abs_values[index+1] - abs_values[index]
            ) / delta_lambda
        elif index == len(wv_values) - 1:
            deriv_results[wv_values[index]] = (
                abs_values[index] - abs_values[index-1]
            ) / delta_lambda
        else:
            deriv_results[wv_values[index]] = (
                abs_values[index + 1] - abs_values[index - 1]
            ) / delta_lambda * 1/2

    return deriv_results


def applies_derivative_on_savgol_values(values_to_derivate: list,
                                        dev_order: int, delta_lambda: int,
                                        derivative: callable) -> list:
    """
    Applies derivative on Savgol Values.
    """
    # How many times this function will calculates derivative?
    # It's depends on the derivative order
    # So, it's a list of derivative functions repeated several times
    # if the derivative order is > 1
    how_many_derivatives = [
        derivative for x in range(dev_order)
    ]

    deriv_results = list()
    for dic in values_to_derivate:
        for func in how_many_derivatives:
            dic = func(dic, delta_lambda)
        deriv_results.append(dic)
    return deriv_results


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
    worksheet = workbook.add_worksheet(f'{filename[:30]}')
    worksheet.write(0, 0, 'nm')
    worksheet.write_column(1, 0, wavelength_range)
    row = 0
    col = 1
    for sample, data in full_values.items():
        worksheet.write(row, col, sample)
        worksheet.write_column(row + 1, col, data)
        col += 1

    # Solve this
    '''# Creates a chart type
    chart = workbook.add_chart({
        'type': 'scatter',
        'subtype': 'smooth'
    })

    # Creates a big list of letters, which represents columns of worksheets
    letters_list = list(ascii_uppercase) + [
        ('A' + letter) for letter in list(ascii_uppercase)
    ] + [
        ('B' + letter) for letter in list(ascii_uppercase)
    ] + [
        ('C' + letter) for letter in list(ascii_uppercase)
    ]

    for i in range(len(full_values.items())):
        chart.add_series({
            'categories': '=Sheet1!$A$2:$A$602',
            'values': '=Sheet1!$B$2:$B$602',
        })

    chart.set_title({'name': f'{filename}'})
    chart.set_x_axis({
        'name': 'nm',
        'min': wavelength_range[0],
        'max': wavelength_range[len(wavelength_range) - 1],
    })
    chart.set_y_axis({
        'name': 'A'
    })
    chart.set_size({
        'width': 650,
        'height': 500
    })
    worksheet.insert_chart('E4', chart)'''


def closes_workbook(workbook):
    workbook.close()


def custom_map(function, sequence):
    """
    Applies a custom map function to a sequence.
    """
    return [
        function(item) for item in sequence
    ]


def organize_data_to_worksheet(derivative_values: list) -> list:
    """
    Function to organize the data into columns to write on worksheets
    """
    # Now derivative_values is a list of lists like this:
    # [[1, 2, 3], [4, 5, 6]]
    # But for write worksheets, I need that the list must be like this:
    # [[1, 4], [2, 5], [3, 6]]
    # For this reason, this line is important:
    derivative_values = list(zip(*derivative_values))

    data_to_be_used_on_worksheet = list()
    for sequence in derivative_values:
        organized_data = dict()
        for key in sequence[0].keys():
            organized_data[key] = tuple(
                organized_data[key] for organized_data in sequence
            )
        data_to_be_used_on_worksheet.append(organized_data)
    return data_to_be_used_on_worksheet


def pipeline(
        files, filename, windowlength, polyorder, savgol_option,
        derivative_option, derivative_order, delta_lambda
        ):

    workbook = creates_workbook(filename)

    csv_data_list = custom_map(read_csv, files)

    filenames = custom_map(get_filename, csv_data_list)

    csv_data_values = custom_map(get_real_values_data, csv_data_list)

    wavelength_range = get_wavelength_range(csv_data_values[0])

    abs_values_list = custom_map(get_absorbance_values, csv_data_values)

    full_results = {
        k: v for k, v in zip(filenames, abs_values_list)
    }

    creates_new_worksheet(workbook, filename, wavelength_range, full_results)

    if savgol_option == 1:
        savgol_values = custom_map(
            lambda x: applies_savgol_filter(x, windowlength, polyorder),
            abs_values_list
            )

        full_savgol_results = {
            k: v for k, v in zip(filenames, savgol_values)
        }

        creates_new_worksheet(
            workbook, f'{filename}savgol',
            wavelength_range, full_savgol_results
        )

    if derivative_option == 1:
        # Prepare data do derivate
        data_to_derivate = custom_map(
            lambda x: prepare_data_to_derivate(
                x, wavelength_range, delta_lambda
            ), savgol_values
        )

        # Calculates derivative
        derivative_values = custom_map(
            lambda x: applies_derivative_on_savgol_values(
                x, derivative_order, delta_lambda, derivate),
            data_to_derivate
        )

        worksheet_data = organize_data_to_worksheet(derivative_values)
        for i, deriv_dict in enumerate(worksheet_data):
            deriv_wavelength_range = deriv_dict.keys()

            deriv_absorbance_previous_values = list(deriv_dict.values())
            deriv_absorbance_values = list(
                zip(*deriv_absorbance_previous_values)
                )

            full_derivative_results = {
                k: v for k, v in zip(filenames, deriv_absorbance_values)
            }

            creates_new_worksheet(
                workbook, f'{filename}deriv{i + 1}',
                deriv_wavelength_range, full_derivative_results
            )

    closes_workbook(workbook)
    delete_temp_data()
