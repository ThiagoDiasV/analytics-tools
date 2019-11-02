from app import app
from flask import (
    render_template, request, redirect,
    url_for, send_from_directory, flash
)
from .forms import PdfUploadForm, CsvUploadForm
import os
from tools.pdf_reader import pipeline
from tools import save_files, delete_temp_data
from tools.csv_reader import read_csv, get_wavelength_range, get_absorbance_values


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hplc_pdf_compiler/', methods=['GET', 'POST'])
def hplc_pdf_compiler():
    form = PdfUploadForm()

    if form.validate_on_submit():

        pdf_files = request.files.getlist('pdf_files')
        result_options = int(request.form['options'])
        form.validate_form(pdf_files)
        files = save_files(pdf_files, '.pdf')

        try:
            pipeline(files, result_options)
        except AttributeError:
            delete_temp_data()
            flash('Você não selecionou um PDF válido')
            return redirect(
                url_for('hplc_pdf_compiler')
                )

        filename = (os.listdir(f'{app.config["WORKSHEETS_FOLDER"]}')[-1])
        return redirect(url_for('download', filename=filename))
    return render_template(
        'hplc_pdf_compiler.html',
        form=form,
        )


@app.route('/<path:filename>/')
def download(filename):
    return send_from_directory(
            directory=app.config["WORKSHEETS_FOLDER"],
            filename=filename,
            as_attachment=True
        )


@app.route('/spectrows_maker/', methods=['GET', 'POST'])
def spectrows_maker():
    form = CsvUploadForm()

    if form.validate_on_submit():
        csv_files = request.files.getlist('csv_files')
        form.validate_form(csv_files)
        files = save_files(csv_files, '.csv')
        file = read_csv(files[0])
        get_wavelength_range(file)
        get_absorbance_values(file)
        return redirect(url_for('spectrows_maker'))
    return render_template(
        'spectrows_maker.html',
        form=form)


@app.route('/visco_report_maker/')
def visco_report_maker():
    return render_template('visco_report_maker.html')
