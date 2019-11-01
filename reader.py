import re
import os
import xlsxwriter
from time import asctime
from app import app
from tika import parser


def read_ocr_with_tika(image):
    text = parser.from_file(image)['content']
    return text


def get_results(text: str, peak_option: int) -> dict:
    """
    Read the text of images using OCR with Pytesseract.
    """

    # RE patterns defined
    pattern = re.compile(
        r'\d{1},\d{3}\s\d*\s\d{1,3},\d{2}\s\d*\s\d{1,3},\d{2}'
        )

    filename_pattern = re.compile(
        r'\\\w+\s?\w+\-?\w+(\s|.dat)'
    )

    filename = re.search(filename_pattern, text).group()
    result_matches = re.findall(pattern, text)

    # Results
    results = []
    # Get only the first part of the readings.
    flag = 0
    peaks_list = []

    if not peak_option:
        for match in result_matches:
            new_flag = float((match.split(' ')[0]).replace(',', '.'))
            if new_flag > flag:
                flag = new_flag
                results.append(match)
            else:
                break
    else:
        for match in result_matches:
            new_peak = float((match.split(' ')[-1]).replace(',', '.'))
            peaks_list.append(new_peak)
        major_peak = max(peaks_list)
        for match in result_matches:
            if float((match.split(' ')[-1]).replace(',', '.')) == major_peak:
                results.append(match)

    return {'sample': filename, 'results': results}


def delete_previous_workbooks():
    """
    In order to maintain empty worksheets folder, this function
    deletes all .xlsx files inside the folder.
    """
    worksheets = [
        f'{app.config["WORKSHEETS_FOLDER"]}/{worksheet}' for worksheet
        in os.listdir(f'{app.config["WORKSHEETS_FOLDER"]}/')
    ]

    for worksheet in worksheets:
        os.remove(worksheet)


def creates_workbook(hplc_values: list) -> xlsxwriter.Workbook:
    """
    Creates a xlxs file with the data.
    """

    # Delete previous workbooks
    delete_previous_workbooks()

    # Get date for the filename
    date = asctime().replace(':', '').replace(' ', '')

    # Creates one workbook
    workbook = xlsxwriter.Workbook(
        f'{app.config["WORKSHEETS_FOLDER"]}/{date}.xlsx'
        )

    # Add a worksheet to the workbook and changes columns width
    worksheet = workbook.add_worksheet('')
    worksheet.set_column(0, 0, 12)
    worksheet.set_column(1, 1, 16)
    worksheet.set_column(2, 5, 12)
    worksheet.set_column(7, 7, 32)

    # Columns labels
    labels = (
        'Amostra', 'Tempo de retenção', 'Área', 'Área (%)',
        'Altura de pico', 'Altura (%)'
    )

    # Writes merchan :)
    worksheet.write(0, 7, 'Criado por')
    worksheet.write(1, 7, 'https://analytics-tools.herokuapp.com')

    # Writes the values at worksheet
    worksheet.write_row(0, 0, labels)
    row = 1
    col = 0
    for sample in hplc_values:
        for value in sample.values():
            if not isinstance(value, list):
                if value.endswith('.dat'):
                    value = value.replace('.dat', '')
                worksheet.write(row, col, value.replace('\\', ''))
                col += 1
            else:
                for result in value:
                    worksheet.write_row(row, col, result.split(' '))
                    row += 1
                col = 0

    # Closes workbook
    workbook.close()

    return workbook


def delete_temp_data():
    """
    Delete temporary PDF files
    """
    pdf_files = [
        f'{app.config["UPLOAD_FOLDER"]}/{file}'
        for file in os.listdir(f'{app.config["UPLOAD_FOLDER"]}')
        if file.endswith('.pdf')
    ]
    for pdf in pdf_files:
        os.remove(pdf)


def pipeline(files: str, peak_option: int):
    """
    Processes the files and creates the workbook using the functions above.
    """

    texts = [
        read_ocr_with_tika(file) for file
        in files
    ]

    results = sorted([
        get_results(text, peak_option) for text
        in texts
    ], key = lambda x: x['sample'])

    # Creates the workbook
    creates_workbook(results)

    delete_temp_data()
