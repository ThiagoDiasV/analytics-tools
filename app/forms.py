from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import SubmitField, MultipleFileField
from wtforms.validators import ValidationError


class PdfUploadForm(FlaskForm):
    pdf_files = MultipleFileField([FileRequired()])

    def validate_form(form, files):
        if not files[0].filename:
            raise ValidationError(
                'Você não inseriu nenhum arquivo'
            )

        for file in files:
            if not file.filename.endswith('.pdf'):
                raise ValidationError(
                    'Você inseriu arquivos que não são PDF'
                )


class CsvUploadForm(FlaskForm):
    csv_files = MultipleFileField([FileRequired()])

    def validate_form(form, files):
        if not files[0].filename:
            raise ValidationError(
                'Você não inseriu nenhum arquivo'
            )

        for file in files:
            if not file.filename.endswith('.csv'):
                raise ValidationError(
                    'Você inseriu arquivos que não são CSV'
                )
