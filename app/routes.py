from app import app
from flask import (
    render_template, request, redirect,
    url_for, send_from_directory, flash
)
from .forms import PdfUploadForm, CsvUploadForm
import os
import tools
from tools import pdf_reader, csv_reader


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hplcpc/', methods=['GET', 'POST'])
def hplcpc():
    form = PdfUploadForm()

    if form.validate_on_submit():

        pdf_files = request.files.getlist('pdf_files')
        result_options = int(request.form['options'])
        form.validate_form(pdf_files)
        filename = request.form['filename_field'].strip().replace(' ', '')
        files = tools.save_files(pdf_files, '.pdf')

        try:
            pdf_reader.pipeline(files, result_options, filename)
        except AttributeError:
            tools.delete_temp_data()
            flash('Você não selecionou um PDF válido')
            return redirect(
                url_for('hplcpc')
                )

        filename = (os.listdir(f'{app.config["WORKSHEETS_FOLDER"]}')[-1])
        return redirect(url_for('download', filename=filename))
    return render_template(
        'hplcpc.html',
        form=form,
        )


@app.route('/<path:filename>/')
def download(filename):
    return send_from_directory(
            directory=app.config["WORKSHEETS_FOLDER"],
            filename=filename,
            as_attachment=True
        )


@app.route('/spectrowsm/', methods=['GET', 'POST'])
def spectrowsm():
    form = CsvUploadForm()

    if form.validate_on_submit():
        csv_files = request.files.getlist('csv_files')
        form.validate_form(csv_files)
        filename = request.form['filename_field'].strip().replace(' ', '')
        # continuar daqui
        windowlength = int(request.form['windowlength'])
        polyorder = int(request.form['polyorder'])
        files = tools.save_files(csv_files, '.csv')
        try:
            csv_reader.pipeline(files, filename, windowlength, polyorder)
        except AttributeError:
            tools.delete_temp_data()
            flash('Você não selecionou um CSV válido')
            return redirect(
                url_for('spectrowsm')
                )
        filename = (os.listdir(f'{app.config["WORKSHEETS_FOLDER"]}')[-1])
        return redirect(url_for('download', filename=filename))
    return render_template(
        'spectrowsm.html',
        form=form)


@app.route('/viscorm/')
def viscorm():
    return render_template('viscorm.html')
