
from enum import Enum


class RuntimeStatus(Enum):
    STARTING = 'STARTING'
    RUNNING = 'RUNNING'
    PAUSED = 'PAUSED'
    DELETED = 'DELETED'
    ERROR = 'ERROR'
