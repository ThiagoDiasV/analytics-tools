from app import app
import os
from werkzeug.utils import secure_filename


def save_files(files: list, extension: str) -> list:
    """
    Save upload files on temp folder.
    """
    # Delete previous PDFs
    delete_temp_data()

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    files = [
        f'{app.config["UPLOAD_FOLDER"]}/{file}' for file
        in os.listdir(app.config["UPLOAD_FOLDER"])
        if file.endswith(f'{extension}')
    ]
    return files


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


def delete_temp_data():
    """
    Delete temporary files.
    """
    files = [
        f'{app.config["UPLOAD_FOLDER"]}/{file}'
        for file in os.listdir(f'{app.config["UPLOAD_FOLDER"]}')
    ]
    for file in files:
        os.remove(file)
