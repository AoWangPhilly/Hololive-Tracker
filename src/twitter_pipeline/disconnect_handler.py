import datetime
from dataclasses import dataclass


@dataclass
class StreamDisconnectHandler:
    connection_break_time: datetime.datetime
    connection_reconnect_time: datetime.date
    stream_break: bool = False

    