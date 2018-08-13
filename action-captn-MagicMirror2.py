#!/usr/bin/env python2
# -*- coding: utf-8 -*-


import ConfigParser
import io
import paho.mqtt.client as mqtt
import json

CONFIGURATION_ENCODING_FORMAT = "utf-8"
CONFIG_INI = "config.ini"

class SnipsConfigParser(ConfigParser.SafeConfigParser):
    def to_dict(self):
        return {section: {option_name: option for option_name, option in self.items(section)} for section in self.sections()}


def read_configuration_file(configuration_file):
    try:
        with io.open(configuration_file, encoding=CONFIGURATION_ENCODING_FORMAT) as f:
            conf_parser = SnipsConfigParser()
            conf_parser.readfp(f)
            return conf_parser.to_dict()
    except (IOError, ConfigParser.Error) as e:
        return dict()


conf = read_configuration_file(CONFIG_INI)
print("Conf:", conf)

# MQTT client to connect to the bus
mqtt_client = mqtt.Client()

def on_connect(client, userdata, flags, rc):
    client.subscribe("hermes/intent/#")
    client.subscribe("hermes/intent/#")


def on_message(client, userdata, msg):

    if 
    data = json.loads(msg.payload.decode("utf-8"))
    session_id = data['sessionId']
    try:
        slots = {slot['slotName']: slot['value']['value'] for slot in data['slots']}
        user, intentname = data['intent']['intentName'].split(':')


        if (intentname == 'MM_Hide' or intentname == 'MM_Show' or intentname == 'MM_Move'):
            module = slots['MODULE']

            if module == 'ALL':
                mode = 'ALL'
            elif 'PAGE' in module:
                mode = 'PAGE'
            else:
                 mode = 'STANDARD'

            if intentname == 'MM_Hide' and (mode == 'STANDARD' or mode == 'ALL'):
                action = {'module':module}
            elif intentname == 'MM_Show' and (mode == 'STANDARD' or mode == 'PAGE') :
                action = {'module':module}
            elif intentname == 'MM_Move' and mode == 'STANDARD':
                position = slots['POSITION']
                action = {'module':module, 'position':position}
            else:
                raise UnboundLocalError("Das kann ich leider nicht")
            say(session_id, "Mache ich")
            MM2(intentname, action)
    except UnboundLocalError, e:
        say(session_id, e.message)

    except KeyError:
                say(session_id, "Ich habe dich leider nicht verstanden.")

def valve_callback(client, userdata, msg):
    say(session_id, "Ich habe dich leider nicht verstanden.")

def MM2(intentname, action):
    mqtt_client.publish(('hermes/external/MagicMirror2/' + intentname),
                        json.dumps(action))

def say(session_id, text):
    mqtt_client.publish('hermes/dialogueManager/endSession',
                        json.dumps({'text': text, "sessionId": session_id}))



if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqttclient.message_callback_add("hermes/intent/#", on_message)
    mqttclient.message_callback_add("hermes/external/MagicMirror2/#", valve_callback)
    #mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", "1883")
    mqtt_client.loop_forever()
