import logging
import socket
import struct
import re

from module.conf import config
from string_utils import is_full_string

logger = logging.getLogger(__name__)
_mac_reg = "^([0-9a-fA-F][0-9a-fA-F]:){5}([0-9a-fA-F][0-9a-fA-F])$"


class Util:
    def __init__(self):
        pass

    @staticmethod
    def can_run() -> bool:
        if config["platform"]["type"] == "bemfa":
            if not is_full_string(config["platform"]["bemfa"]["topic"]):
                return False
            if not is_full_string(config["platform"]["bemfa"]["private_key"]):
                return False
            return True
        if config["platform"]["type"] == "diandeng":
            return True

        return False

    @staticmethod
    def wake_on_lan(broadcast_ip, mac_address):
        found = re.fullmatch(_mac_reg, mac_address)
        if found:
            # If the match is found, remove mac separator [:-\s]
            _mac_address = mac_address.replace(mac_address[2], "")
        else:
            raise ValueError("Incorrect MAC address format")

        logger.debug(
            f"Wake on lan broadcast_ip: {broadcast_ip}, mac_address: {mac_address}"
        )

        # Pad the synchronization stream.
        data = "".join(["FFFFFFFFFFFF", _mac_address * 20])
        send_data = b""

        # Split up the hex values and pack.
        for j in range(0, len(data), 2):
            send_data = b"".join(
                [send_data, struct.pack("B", int(data[j : j + 2], 16))]
            )

        # Broadcast it to the LAN.
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sock.sendto(send_data, (broadcast_ip, 7))
