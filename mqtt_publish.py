import paho.mqtt.client as mqtt

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print("Connected to MQTT broker")
    else:
        print("Failed to connect, return code: " + str(rc))


client = mqtt.Client()

client.on_connect = on_connect

broker_address = "localhost"
topic = "Asutosh"

client.connect(broker_address, 1883, 60)

while True:
    message = input("Enter a message (or 'q' to quit): ")
    if message == 'q':
        break
    client.publish(topic, message)

client.disconnect()