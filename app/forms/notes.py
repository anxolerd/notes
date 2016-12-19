from wtforms.fields.core import StringField, SelectField
from wtforms.fields.simple import TextAreaField
from wtforms.form import Form
from wtforms.validators import DataRequired, Length


class NoteForm(Form):
    title = StringField(
        label='Title',
        validators=[DataRequired(), Length(min=3)],
    )

    text = TextAreaField(
        label='Text',
        validators=[DataRequired()],
    )

    category = SelectField(
        label='Category',
        validators=[DataRequired()],
        coerce=int,
    )
