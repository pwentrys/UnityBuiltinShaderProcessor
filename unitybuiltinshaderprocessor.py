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
target = Path(str(paths.target) + r'\\')
files = {}

for EXTENSION in EXTENSIONS:
    files[EXTENSION] = []

for root, dirnames, filenames in os.walk(str(source)):
    root_target = str(root).replace('\\source\\', '\\target\\')
    # print(f'Root: {root}')
    # print(f'Root_Target: {root_target}')
    # paths.mkdir_ifnexist(root_target)
    # for dirname in dirnames:
    #    print(f'--- Dir: {root}\\{dirname}')
    for filename in filenames:
        file = Path(f'{root}\\{filename}')
        files[ext_enum.get_type_from_path(file)].append(file)
        # print(f'--- FileName: {root}\\{filename}')


# for filearray in files:
#    print(f'------------ {filearray} ({len(files[filearray])})- START ------------')
#    for file in files[filearray]:
#        print(f'--- {file}')
#    print(f'------------ {filearray} - END ------------\n\n')
