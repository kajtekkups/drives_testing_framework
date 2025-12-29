from dataclasses import dataclass
from enum import Enum

@dataclass
class ServerDef:
    id: str         # unique slug for matching callbacks
    name: str       # display name
    kind: str       # "Drive" / "MQTT" / "OPC UA" / etc.
    url: str        # endpoint or URI


class ServerId(str, Enum):
    motor_drive = "drive-1"
    load_drive = "drive-2"
    mqtt_1 = "mqtt-1"


SERVERS: list[ServerDef] = [
    ServerDef(id=ServerId.motor_drive, name="Drive 1", kind="Drive", url=""),
    ServerDef(id=ServerId.load_drive, name="Drive 2", kind="Drive", url=""),
    # ServerDef(id=ServerId.mqtt_1,  name="MQTT",    kind="MQTT", url="")
]



@dataclass
class Connectionstatus:
    ip: str
    connected:  bool
