from enum import Enum

class DatasetState(Enum):
    SPLIT_INIT = "on_split_init"
    SPLIT_END = "on_split_end"
    SPLIT_DF = "split_method_df"
    SPLIT_DIR = "split_method_dir"