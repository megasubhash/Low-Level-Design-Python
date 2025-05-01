from enum import Enum

class CommandType(Enum):
    INSERT = "INSERT"
    DELETE = "DELETE"
    REPLACE = "REPLACE"
    UNDO = "UNDO"
    REDO = "REDO"
    SAVE = "SAVE"
    LOAD = "LOAD"
    FIND = "FIND"
    FIND_REPLACE = "FIND_REPLACE"
