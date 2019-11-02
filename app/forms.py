from flask_wtf import FlaskForm
from flask_wtf.file import FileRequired
from wtforms import MultipleFileField
from wtforms.fields import StringField, SelectField
from wtforms.validators import ValidationError, DataRequired, Length


class PdfUploadForm(FlaskForm):
    pdf_files = MultipleFileField([FileRequired()])
    filename_field = StringField('Nome do arquivo de saída', validators=[
        DataRequired(), Length(min=1, max=20, message=None)
    ])

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
    filename_field = StringField('Nome do arquivo de saída', validators=[
        DataRequired(), Length(min=1, max=20, message=None)
    ])

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
