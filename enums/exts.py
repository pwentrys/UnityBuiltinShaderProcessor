from enum import Enum
from os.path import splitext


# TODO Improve Functionality
# File extensions we care about.
class EXTENSIONS(Enum):
    CGINC = 1
    CS = 2
    GLSLINC = 3
    SHADER = 4
    TXT = 5


EXTENSIONS_STRINGS = {}
for ext in EXTENSIONS:
    EXTENSIONS_STRINGS[f'.{(str(ext).split(".")[1]).lower()}'] = ext


def get_str_from_enum(num):
    return EXTENSIONS_STRINGS[num]


def get_type_from_path(path):
    return EXTENSIONS_STRINGS[splitext(path)[1]]
