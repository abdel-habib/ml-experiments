from enum import Enum

class DatasetState(Enum):
    SPLIT_INIT = "on_split_init"
    SPLIT_END = "on_split_end"