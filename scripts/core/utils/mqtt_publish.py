import paho.mqtt.client as mqtt
from loguru import logger


class MQTTPublisher:
    def __init__(self, message, topic):
        self.message = message
        self.topic = topic

    def publish(self):
        def on_connect(client, userdata, flags, rc):
            if rc == 0:
                logger.info("Connected to MQTT broker")
                self.publish_success = True
            else:
                logger.info("Failed to connect, return code: " + str(rc))
                self.publish_success = False

        client = mqtt.Client()

        client.on_connect = on_connect

        broker_address = "localhost"
        topic = f"Fedex_{self.topic}"

        client.connect(broker_address, 1883, 300)
        result = client.publish(topic, self.message)

        client.disconnect()

        print(self.publish_success if result[0] == mqtt.MQTT_ERR_SUCCESS else False)
        print(mqtt.MQTT_ERR_SUCCESS)
        print(result[0])