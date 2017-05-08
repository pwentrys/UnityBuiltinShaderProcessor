from pathlib import Path

import enums.exts as ext_enum


class FILEBASE:
    def __init__(self, path):
        self.path = Path(path)
        self.ext_type = ext_enum.get_type_from_path(self.path)

    def __log__(self):
        print(f'Path: {self.path}\nType: {self.ext_type}')
