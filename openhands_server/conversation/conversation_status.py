
from enum import Enum


class ConversationStatus(Enum):
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    STOPPED = 'STOPPED'
    ERROR = 'ERROR'
