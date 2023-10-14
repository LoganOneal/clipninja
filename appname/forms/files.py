from appname.forms import BaseForm
from wtforms import validators, TextAreaField, FileField, StringField

class FileForm(BaseForm):
    title = StringField('Project Title')
    description = TextAreaField('Description')
    attachment = FileField('Attachment', validators=[validators.InputRequired()])
