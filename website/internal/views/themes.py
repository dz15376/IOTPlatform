from flask import render_template, request, jsonify

import data_interface
from internal import internal_site
from utilities.session import get_active_user


@internal_site.route('/add_theme')
def add_theme():
    devices = data_interface.get_user_devices(get_active_user()['user_id'])
    rooms = data_interface.get_user_default_rooms()
    rooms = sorted(rooms, key=lambda k: k['name'])
    return render_template("internal/add_theme.html", devices=devices,
                           rooms=rooms)


@internal_site.route('/new_theme', methods=['POST', 'GET'])
def new_theme():
    theme_devices = request.get_json()
    return jsonify(theme_devices)


@internal_site.route('/themes')
def themes():
    devices = {}
    themes = data_interface.get_user_themes(get_active_user()['user_id'])
    for theme in themes:
        for device in theme['settings']:
            devices[device['device_id']] = (data_interface.get_device_info(device['device_id']))['name']
            if (data_interface.get_device_info(device['device_id']))['device_type'] == 'light_switch':
                lights = data_interface.get_device_info(device['device_id'])
    return render_template("internal/themes.html", themes=themes, upperdev=devices, lights=lights)
