#! /usr/bin/python3

import pulsectl
import json

device_icons = { "headset": "", "headphone": "", "default": "" }

pulse = pulsectl.Pulse('audio-info')

default_sink = pulse.get_sink_by_name(pulse.server_info().default_sink_name)

description = default_sink.description
form_factor = default_sink.proplist.get('device.form_factor', 'speaker')

print(json.dumps({ "name": description, "icon": device_icons.get(form_factor, device_icons["default"]) }))
