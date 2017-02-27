from flask import render_template

from main import app
import data_interface
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField
import views.devices
import views.rooms
import views.admin
from views.forms import AddNewRoomForm

@app.route('/triggers')
def triggers():
    return render_template("triggers.html")


@app.route('/')
def index(add_new_room_form=None):
    if add_new_room_form is None:
        add_new_room_form = AddNewRoomForm()
    rooms = data_interface.get_user_default_rooms()
    return render_template("home.html", rooms=rooms, new_room_form=add_new_room_form)


@app.route('/admin/user/<string:user_id>')
def admin_index(user_id):
    rooms = data_interface.get_default_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    return render_template("home.html", admin=True, rooms=rooms, user_name=user_info["name"])


@app.route('/logout')
def logout():
    return "To be implemented"


@app.route('/account/settings')
def account_settings():
    return "To be implemented"


@app.route('/help')
def help():
    return render_template("help.html")


status = ['Enabled', 'Disabled']
themeinfo = [{'id': '1', 'name': 'Weekend Away Theme', 'theme_status': status[0]},
             {'id': '2', 'name': 'Night Party Theme', 'theme_status': status[1]}]


@app.route('/themes')
def themes():
    return render_template("themes.html", themeinfo=themeinfo, status=status)
