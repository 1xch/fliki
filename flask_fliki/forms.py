from flask import current_app
from flask.ext.wtf import Form
from wtforms import (HiddenField, TextField, TextAreaField, SubmitField)
from wtforms.validators import (InputRequired, ValidationError)
from werkzeug.local import LocalProxy
from .util import _wiki, clean_url


class WikiForm(Form):
    def __init__(self, **kwargs):
        super(WikiForm, self).__init__(**kwargs)


class EditorForm(WikiForm):

    pagekey = HiddenField('')
    edit_content = TextAreaField('')
    submit = SubmitField('create or save page')

    def __init__(self, **kwargs):
        super(EditorForm, self).__init__(**kwargs)
        self.key = clean_url(kwargs.get('url', None))
        self.pagekey.data = self.key


class MoveForm(WikiForm):

    oldkey = HiddenField('')
    newkey = TextField('')
    submit = SubmitField('move page')

    def __init__(self, **kwargs):
        super(MoveForm, self).__init__(**kwargs)
        self.oldkey.data = kwargs.get('old', None)
        self.newkey.data = kwargs.get('new', None)


class DeleteForm(WikiForm):

    delete = HiddenField('')
    submit = SubmitField('delete page')

    def __init__(self, **kwargs):
        super(DeleteForm, self).__init__(**kwargs)
        self.delete.data = kwargs.get('delete', None)
