from flask.ext.wtf import Form
from wtforms import (TextField, TextAreaField, PasswordField)
from wtforms.validators import (InputRequired, ValidationError)

class URLForm(Form):
    url = TextField('', [InputRequired()])

    def validate_url(form, field):
        if wiki.exists(field.data):
            raise ValidationError('The URL "%s" exists already.' % field.data)

    def clean_url(self, url):
        return Processors().clean_url(url)

#class SearchForm(Form):
#    term = TextField('', [InputRequired()])

class EditorForm(Form):
    title = TextField('', [InputRequired()])
    body = TextAreaField('', [InputRequired()])
    tags = TextField('')
