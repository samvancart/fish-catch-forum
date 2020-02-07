from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,DecimalField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class FishForm(FlaskForm):
    species = StringField("Species", [validators.Length(min=2)])
    weight = DecimalField("Weight (kg)")
    picture = FileField('Fish picture',validators=[FileAllowed(['jpg','png'])])

    class Meta:
        csrf = False
