from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed
from wtforms import StringField,DecimalField,validators
from wtforms.validators import DataRequired, Length, Email, EqualTo, ValidationError



class FishForm(FlaskForm):
    species = StringField("Species", [validators.Length(min=2,max=20)])
    weight = DecimalField("Weight (kg)",[validators.NumberRange(min=0.001,max=25000)])
    picture = FileField('Fish picture',validators=[FileAllowed(['jpg','png'])])

    class Meta:
        csrf = False
