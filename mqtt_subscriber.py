import paho.mqtt.client as mqtt


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("Asutosh")


def on_message(client, userdata, msg):
    print("Received message: " + msg.payload.decode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

broker_address = "localhost"
client.connect(broker_address, 1883, 60)

client.loop_forever()