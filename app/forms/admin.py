from wtforms.form import Form
from wtforms.fields import StringField
from wtforms.fields import FieldList
from wtforms.validators import DataRequired
from wtforms.validators import Length


class CategoryForm(Form):
    name = StringField(
        label='Name',
        validators=[DataRequired(), Length(min=3)],
    )
    allowed_roles = FieldList(
        unbound_field=StringField(),
        label='Allowed roles',
        validators=[Length(min=1), DataRequired()],
        min_entries=1,
        max_entries=5,
    )
