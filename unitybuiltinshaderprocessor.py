import os
from pathlib import Path

import enums.exts as ext_enum
from enums.exts import EXTENSIONS
# from models.filebase import FILEBASE
from paths import Paths

# from datetime import datetime


# start_time = datetime.utcnow()

paths = Paths(__file__)
# paths.__log__()

source = paths.source
# target = Path(str(paths.target) + r'\\')
files = {}

for EXTENSION in EXTENSIONS:
    files[EXTENSION] = []

# Sort all the files.
for root, dirnames, filenames in os.walk(str(source)):
    # root_target = str(root).replace('\\source\\', '\\target\\')
    for filename in filenames:
        file = Path(f'{root}\\{filename}')
        files[ext_enum.get_type_from_path(file)].append(file)

for filearray in files:
    if filearray is EXTENSIONS.CGINC:
        for file in files[filearray]:
            current_file = Path(str(file))
            text_in = current_file.read_text()
            lines = text_in.splitlines()
            tab_depth = 0
            text_out = ''
            for line in lines:

                while line.__contains__('defined '):
                    line = line.replace('defined ', 'defined')
                while line.__contains__('  '):
                    line = line.replace('  ', ' ')
                while line.__contains__('# '):
                    line = line.replace('# ', '#')

                if line.__contains__(r'#el') or line.__contains__(r'#end') or line.__contains__(r'}'):
                    tab_depth = tab_depth - 1
                if tab_depth > 0:
                    d = tab_depth
                    while d > 0:
                        line = '\t' + line
                        d -= 1

                # print(f'{depth} - {line}')

                if line.__contains__(r'#if') or line.__contains__(r'#el') or line.__contains__(r'{'):
                    tab_depth = tab_depth + 1

                text_out += f'{line}\n'

            new_file = Path(str(file).replace("\source\\", "\\target\\"))
            paths.mkdir_ifnexist_bypath(new_file)
            new_file.write_text(text_out)
