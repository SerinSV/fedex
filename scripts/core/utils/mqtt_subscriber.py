import paho.mqtt.client as mqtt
from loguru import logger


def on_connect(client, userdata, flags, rc):
    print("Connected with result code " + str(rc))

    client.subscribe("Fedex_#")


def on_message(client, userdata, msg):
    logger.info("Received message: " + msg.payload.decode())


client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

broker_address = "localhost"
client.connect(broker_address, 1883, 300)

client.loop_forever()