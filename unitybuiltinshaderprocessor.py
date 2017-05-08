import os
from pathlib import Path

from models.filebase import FILEBASE
from paths import Paths

# from datetime import datetime


# start_time = datetime.utcnow()

paths = Paths(__file__)
# paths.__log__()

source = paths.source
target = Path(str(paths.target) + r'\\')
files = []

for root, dirnames, filenames in os.walk(str(source)):
    root_target = str(root).replace('\\source\\', '\\target\\')
    # print(f'Root: {root}')
    # print(f'Root_Target: {root_target}')
    # paths.mkdir_ifnexist(root_target)
    # for dirname in dirnames:
    #    print(f'--- Dir: {root}\\{dirname}')
    for filename in filenames:
        files.append(FILEBASE(filename))
        # print(f'--- FileName: {root}\\{filename}')

# print(target)

for file in files:
    file.__log__()
