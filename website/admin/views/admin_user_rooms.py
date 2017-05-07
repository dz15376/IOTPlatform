from flask import redirect, url_for, flash, render_template

import data_interface
from admin import admin_site
from shared.forms import AddNewRoomForm


@admin_site.route('/user/<string:user_id>')
def user(user_id):
    rooms = data_interface.get_rooms_for_user(user_id)
    user_info = data_interface.get_user_info(user_id)
    form = AddNewRoomForm()
    devices = []
    len_rooms = [len(rooms)]
    room_no = [0]
    for room in rooms:
        devices.append(data_interface.get_room_devices(room['room_id']))
    for room in devices:
        for device in room:
            if devices[0][0]['status']['last_temperature'] < 5:
                temp_color = "black"
            elif devices[0][0]['status']['last_temperature'] < 10:
                temp_color = "#1d40c1"
            elif devices[0][0]['status']['last_temperature'] < 15:
                temp_color = '#04abd1'
            elif devices[0][0]['status']['last_temperature'] < 20:  # not too visible against white b/g
                temp_color = '#0ddb66'
            elif devices[0][0]['status']['last_temperature'] < 25:
                temp_color = '#f6f918'
            elif devices[0][0]['status']['last_temperature'] < 30:
                temp_color = '#f95717'
            else:
                temp_color = '#ff0000'
    return render_template("admin/admin_user_home.html", new_room_form=form, admin=True, rooms=rooms, user=user_info,
                           user_name=user_info["name"], room_no=room_no, len_rooms=len_rooms, devices=devices, temp_color=temp_color)


@admin_site.route('/user/<string:user_id>/room/add', methods=['POST', 'GET'])
def add_new_room(user_id):
    form = AddNewRoomForm()
    if form.validate_on_submit():
        try:
            data_interface.add_new_room(user_id=user_id, name=form.name.data)
        except Exception:
            flash("Error", "danger")
            return render_template("admin/admin_new_room.html", new_room_form=form)
        flash("New room successfully added!", 'success')
        return redirect(url_for('.user', user_id=user_id))
    return render_template("admin/admin_new_room.html", new_room_form=form)


@admin_site.route('/user/<string:user_id>/room/<string:room_id>')
def view_room(user_id, room_id):
    user = data_interface.get_user_info(user_id)
    room = data_interface.get_room_info(room_id)
    all_devices = data_interface.get_user_devices(user_id)
    linked_devices = [d for d in all_devices if d['room_id'] is not None]
    unlinked_devices = [d for d in all_devices if d['room_id'] is None]
    room_devices = [d for d in all_devices if d['room_id'] == room_id]
    thermostats = [d for d in room_devices if d['device_type'] == "thermostat"]
    light_switches = [d for d in room_devices if d['device_type'] == "light_switch"]
    door_sensors = [d for d in room_devices if d['device_type'] == "door_sensor"]
    motion_sensors = [d for d in room_devices if d['device_type'] == "motion_sensor"]
    return render_template("admin/admin_roomview.html", user=user, room=room, thermostats=thermostats,
                           light_switches=light_switches,
                           door_sensors=door_sensors, motion_sensors=motion_sensors, unlinked_devices=unlinked_devices,
                           linked_devices=linked_devices)


@admin_site.route('/user/<string:user_id>/room/<string:room_id>/device/<string:device_id>/link')
def link_device_to_room(user_id, room_id, device_id):
    data_interface.link_device_to_room(room_id, device_id)
    flash("Device was successfully linked by Admin!", "success")
    return redirect(url_for('.view_room', user_id=user_id, room_id=room_id))
