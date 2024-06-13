from enum import Enum, auto


class Environment(Enum):
    PRODUCTION = auto()
    SANDBOX = auto()
    STAGING = auto()
    DEVELOPMENT = auto()
