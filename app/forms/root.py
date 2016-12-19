from wtforms.fields.core import StringField, IntegerField
from wtforms.fields.simple import PasswordField
from wtforms.form import Form
from wtforms.validators import DataRequired, ValidationError
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


class ProfileForm(Form):

    username = StringField(
        label='Username',
        validators=[DataRequired()],
    )

    password = PasswordField(
        label='Password',
        validators=[DataRequired()],
    )

    password2 = PasswordField(
        label='Repeat password',
        validators=[DataRequired()],
    )

    first_name = StringField(
        label='First name',
        validators=[DataRequired()],
    )

    middle_name = StringField(
        label='Middle name',
    )

    last_name = StringField(
        label='Last name',
        validators=[DataRequired()],
    )

    def validate_password2(self, field):
        if self.password.data != self.password2.data:
            raise ValidationError('Password should match')
