import os


class Config:
    SECRET_KEY = os.environ.get('SECRET_KEY')
    BASE_DIR = os.getcwd()

    if not os.path.exists(f'{BASE_DIR}/temp/uploads'):
        os.makedirs(f'{BASE_DIR}/temp/uploads')
    if not os.path.exists(f'{BASE_DIR}/temp/worksheets'):
        os.makedirs(f'{BASE_DIR}/temp/worksheets')

    UPLOAD_FOLDER = f'{BASE_DIR}/temp/uploads'
    IMAGES_FOLDER = f'{BASE_DIR}/temp/images'
    WORKSHEETS_FOLDER = f'{BASE_DIR}/temp/worksheets'
