from wtforms.fields.core import StringField, IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form
from wtforms.validators import DataRequired
from wtforms.widgets.core import HiddenInput


class LoginForm(Form):
    username = StringField(
        label='Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        label='Password',
        validators=[DataRequired()],
    )

    key = IntegerField(
        label='Value',
        validators=[DataRequired()],
        widget=HiddenInput(),
    )

    answer = IntegerField(
        label='Answer to the function',
        validators=[DataRequired()],
    )
