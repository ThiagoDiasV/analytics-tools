from app import app
from flask import (
    render_template, request, redirect,
    url_for, send_from_directory, flash
)
from .forms import PdfUploadForm
import os
from werkzeug.utils import secure_filename
from reader import pipeline, delete_temp_data


@app.route('/', methods=['GET'])
@app.route('/index/', methods=['GET'])
def index():
    return render_template('index.html')


@app.route('/hplc_pdf_compiler/', methods=['GET', 'POST'])
def hplc_pdf_compiler():
    form = PdfUploadForm()

    if form.validate_on_submit():
        pdf_files = request.files.getlist('pdf_files')
        form.validate_form(pdf_files)
        for file in pdf_files:
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        files = [
            f'{app.config["UPLOAD_FOLDER"]}/{file}' for file
            in os.listdir(app.config["UPLOAD_FOLDER"])
            if file.endswith('.pdf')
        ]
        result_options = int(request.form['options'])
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


@app.route('/hplc_pdf_compiler/<path:filename>/')
def download(filename):
    return send_from_directory(
            directory=app.config["WORKSHEETS_FOLDER"],
            filename=filename,
            as_attachment=True
        )


@app.route('/spectrows_maker/')
def spectrows_maker():
    return render_template('spectrows_maker.html')


@app.route('/visco_report_maker/')
def visco_report_maker():
    return render_template('visco_report_maker.html')
