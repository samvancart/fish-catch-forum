from flask_wtf import FlaskForm
from wtforms import StringField,DecimalField,validators


class FishForm(FlaskForm):
    species = StringField("Species", [validators.Length(min=2)])
    weight = DecimalField("Weight (kg)")

    class Meta:
        csrf = False
