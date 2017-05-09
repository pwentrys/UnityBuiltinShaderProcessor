import os
from pathlib import Path

import enums.exts as ext_enum
from enums.contains_terms import CONTAINS_TERMS
from enums.exts import EXTENSIONS
from paths import Paths

# from datetime import datetime


# start_time = datetime.utcnow()

paths = Paths(__file__)
# paths.__log__()

source = paths.source
# target = Path(str(paths.target) + r'\\')
file_arrays = {}

for EXTENSION in EXTENSIONS:
    file_arrays[EXTENSION] = []

# Sort all the files.
for root, dirnames, filenames in os.walk(str(source)):
    # root_target = str(root).replace('\\source\\', '\\target\\')
    for filename in filenames:
        file = Path(f'{root}\\{filename}')
        file_arrays[ext_enum.get_type_from_path(file)].append(file)

# TODO organize loc.
# Lazy ref
space = ' '
blank = ''

# TODO Find cozy home.
contains_terms_dict = {
    CONTAINS_TERMS.SPACE: ['defined', space, '#'],
    CONTAINS_TERMS.DEPTH_DECREASE: [r'#el', r'#end', r'}'],
    CONTAINS_TERMS.DEPTH_INCREASE: [r'#if', r'#el', r'{']
}


# TODO Find cozy home.
def contains_term_from_arr(name, terms):
    for term in terms:
        if name.__contains__(term):
            return True
    return False


# TODO Cleanup and organize loc.
def format_write_text(old_file, new_file):
    text_in = old_file.read_text()
    lines = text_in.splitlines()
    tab_depth = 0
    text_out = blank
    for line in lines:

        for term in contains_terms_dict[CONTAINS_TERMS.SPACE]:
            while line.__contains__(term + space):
                line = line.replace(term + space, term)

        if contains_term_from_arr(line, contains_terms_dict[CONTAINS_TERMS.DEPTH_DECREASE]):
            tab_depth = tab_depth - 1
        if tab_depth > 0:
            d = tab_depth
            while d > 0:
                line = f'\t{line}'
                d -= 1

        if contains_term_from_arr(line, contains_terms_dict[CONTAINS_TERMS.DEPTH_INCREASE]):
            tab_depth = tab_depth + 1

        text_out += f'{line}\n'

    new_file.write_text(text_out)


# TODO Cleanup and organize loc.
def ensure_exists(old_file, new_file):
    paths.mkdir_ifnexist_bypath(old_file)
    paths.mkdir_ifnexist_bypath(new_file)


# TODO Cleanup and organize loc.
def format_filenames(path):
    return Path(str(path)), Path(str(path).replace("\source\\", "\\target\\"))


op_arrays_dict = {
    EXTENSIONS.CGINC: [ensure_exists, format_write_text],
    EXTENSIONS.CS: [],
    EXTENSIONS.GLSLINC: [],
    EXTENSIONS.SHADER: [],
    EXTENSIONS.TXT: []
}

processed_files = []

# TODO this is stupid. Remind self how to iterate python.
for file_array in file_arrays:
    for file in file_arrays[file_array]:
        old_file, new_file = format_filenames(file)
        for op in op_arrays_dict[file_array]:
            op(old_file, new_file)
        processed_files[file_array].append(new_file)
