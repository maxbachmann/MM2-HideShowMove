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


def on_message(client, userdata, msg):
    data = json.loads(msg.payload.decode("utf-8"))
    try:
        slots = {slot['slotName']: slot['value']['value'] for slot in data['slots']}
        user, intentname = data['intent']['intentName'].split(':')
        session_id = data['session_id']

        if intentname == 'MM_Hide' or intentname == 'MM_Show' :
            module = slots['MODULE']
            action = {'module':module}
            MM2(intentname, action)
        if intentname == 'MM_Move':
            module = slots['MODULE']
            position = slots['POSITION']
            action = {'module':module, 'position':position}
            MM2(intentname, action)
        say(session_id, "Mache ich")
    except KeyError:
                say(session_id, "Ich habe dich leider nicht verstanden.")




def MM2(intentname, action):
    mqtt_client.publish(('hermes/MagicMirror2/' + intentname),
                        json.dumps(action))

def say(session_id, text):
    mqtt_client.publish('hermes/dialogueManager/endSession',
                        json.dumps({'text': text, "sessionId": session_id}))



if __name__ == "__main__":
    mqtt_client.on_connect = on_connect
    mqtt_client.on_message = on_message
    mqtt_client.connect("localhost", "1883")
    mqtt_client.loop_forever()
