


from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
from wtforms.validators import Length

class AddNewRoomForm(FlaskForm):
    name = StringField("Room name",[Length(min=4, max=10)])
    submit = SubmitField()