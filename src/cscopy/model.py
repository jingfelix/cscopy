import enum


class SearchType(enum.Enum):
    C_SYMBOL = 0
    GLOBAL_DEFINITION = 1
    FUNC_CALLED_BY = 2
    FUNC_CALLING = 3
    TEXT_STRING = 4
    CHANGE_TEXT_STRING = 5
    EGREP = 6
    FILE = 7
    FILES_INCLUDING = 8
    ASSIGN_TO_SYMBOL = 9
