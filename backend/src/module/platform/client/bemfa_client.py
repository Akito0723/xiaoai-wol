import logging

from module.conf import config
from module.utils import Util
from paho.mqtt import client as mqtt_client

logger = logging.getLogger(__name__)


def _message_handler(client, userdata, msg):
    _topic = msg.topic
    _msg = str(msg.payload.decode('utf-8'))
    logger.info(f"Message handler, topic:{_topic}, message: {_msg}")
    if _msg == "on":
        Util.wake_on_lan(config["wol_target"]["broadcast_ip"], config["wol_target"]["mac_address"])
        logger.info("Broadcast magic packet success.")


class BemfaClient:
    def __init__(self):
        self._broker = config["platform"]["bemfa"]["broker"]
        self._private_key = config["platform"]["bemfa"]["private_key"]
        self._tls_port = config["platform"]["bemfa"]["tls_port"]
        self._port = config["platform"]["bemfa"]["port"]
        self._topic = config["platform"]["bemfa"]["topic"]
        # 初始化 MQTT 客户端
        self._client = mqtt_client.Client(client_id=self._private_key)
        self._client.on_connect = self.__on_connect
        self._client.on_disconnect = self._on_disconnect
        self._client.on_subscribe = self._on_subscribe
        self._client.on_message = _message_handler

        self._subscribeFlag = False

    def start(self):
        logger.info(f"Start connected to Bemfa MQTT Broker: {self._broker}")
        # 连接到 Broker
        self._client.connect(self._broker, self._port, keepalive=60)
        self._client.loop_forever()

    def stop(self):
        logger.info(f"Start disconnect Bemfa MQTT Broker: {self._broker}")
        self._client.disconnect()

    def __on_connect(self, client, userdata, flags, rc):
        if rc == 0:
            logger.info(f"Connected to Bemfa Broker: {self._broker} success!")
            # 连接成功后订阅 topic
            self._client.subscribe(self._topic, qos=1)
        else:
            logger.error(f"Failed to connect Bemfa Broker: {self._broker}, return code {rc}")

    def _on_subscribe(self, client, userdata, mid, granted_qos):
        self._subscribeFlag = True
        logger.info(f"Subscribed Bemfa Broker: {self._broker} success, qos = %d" % granted_qos)

    def _on_disconnect(self, client, userdata, reason_code, properties=None):
        logger.info(f"Disconnect Bemfa MQTT Broker: {self._broker} with result code {reason_code}")
