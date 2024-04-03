import socket
import time
import math
from paho.mqtt import client as mqtt_client


#mqtt configs
broker = 'broker.emqx.io'
port = 1883
topic = "holoarm/braco"
# generate client ID with pub prefix randomly
client_id = f'python-mqtt-holo-arm-server'
username = 'emqx'
password = 'public'

# arm configs
HOST = "192.168.15.2" # The remote host
PORT = 30002 # The same port as used by the server

def connect_mqtt() -> mqtt_client:
    def on_connect(client, userdata, flags, rc):
        if rc == 0:
            print("Connected to MQTT Broker!")
        else:
            print("Failed to connect, return code %d\n", rc)

    client = mqtt_client.Client(mqtt_client.CallbackAPIVersion.VERSION1, client_id)
    client.username_pw_set(username, password)
    client.on_connect = on_connect
    client.connect(broker, port)
    return client

def subscribe(client: mqtt_client):
    def on_message(client, userdata, msg):
        print(f"Received `{msg.payload.decode()}` from `{msg.topic}` topic")
        controls = str(msg.payload.decode()).split(" ")
        PI = math.pi
        base = -0.5*PI
        shoulder = -0.5*PI #control 1
        elbow = -0.5*PI
        wrist_1 = -0.5*PI
        wrist_2 = 0.0*PI # control 4
        wrist_3 = 0.25*PI
        for control in controls:
            control = control.split("=")
            if control[0] == "control1":
                shoulder = control[1]
            elif control[0] == "control2":
                elbow = control[1]
            elif control[0] == "control3":
                wrist_1 = control[1]
            elif control[0] == "control4":
                wrist_2 = control[1]

        msg = f"movej([{base}, {shoulder}, {elbow}, {wrist_1}, {wrist_2}, {wrist_3}], a=1.4, v=1.05, t=0, r=0)" + "\n"
        s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        s.connect((HOST, PORT))
        s.send(msg.encode())
        print(msg)
        time.sleep(10)
    client.subscribe(topic)
    client.on_message = on_message


def run():
    client = connect_mqtt()
    subscribe(client)
    client.loop_forever()


if __name__ == '__main__':
    run()

