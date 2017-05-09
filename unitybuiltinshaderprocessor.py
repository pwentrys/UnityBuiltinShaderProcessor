import os
from datetime import datetime
from pathlib import Path

import enums.exts as ext_enum
from config import ADB_LOCATION, FILENAME_PREFIX, UNITY_TEST_PROJECT_INCLUDED
from enums.contains_terms import CONTAINS_TERMS
from enums.exts import EXTENSIONS
from paths import Paths

start_time = datetime.utcnow()

paths = Paths(__file__)
# paths.__log__()

source = paths.source
# target = Path(str(paths.target) + r'\\')
file_lists = {}

for EXTENSION in EXTENSIONS:
    file_lists[EXTENSION] = []

# Sort all the files.
for root, dirnames, filenames in os.walk(str(source)):
    # root_target = str(root).replace('\\source\\', '\\target\\')
    for filename in filenames:
        file = Path(f'{root}\\{filename}')
        file_lists[ext_enum.get_type_from_path(file)].append(file)

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
def contains_term_from_list(name, terms):
    for term in terms:
        if name.__contains__(term):
            return True
    return False


ifdef_original = []
ifdef_updated = []


# TODO Cleanup and organize loc.
def format_write_text_first(old_file, new_file):
    """
    First pass, mimics Unity's formatting.
    Completes
    :param old_file: = old path
    :param new_file: = new path
    :return:
    """
    text_in = old_file.read_text()
    lines = text_in.splitlines()
    tab_depth = 0
    text_out = blank
    first_ifdef_recorded = False
    for line in lines:

        for term in contains_terms_dict[CONTAINS_TERMS.SPACE]:
            while line.__contains__(term + space):
                line = line.replace(term + space, term)

        if contains_term_from_list(line, contains_terms_dict[CONTAINS_TERMS.DEPTH_DECREASE]):
            tab_depth = tab_depth - 1

        if tab_depth > 0:
            d = tab_depth
            while d > 0:
                line = f'\t{line}'
                d -= 1

        if contains_term_from_list(line, contains_terms_dict[CONTAINS_TERMS.DEPTH_INCREASE]):
            if not first_ifdef_recorded and line.__contains__(r'#ifndef'):
                first_ifdef_recorded = True
                ifdef_original_term = line.replace('#ifndef', blank)

                while ifdef_original_term.__contains__(space):
                    ifdef_original_term = ifdef_original_term.replace(space, blank)

                ifdef_original.append(ifdef_original_term)

                ifdef_updated_term = f'{FILENAME_PREFIX.upper()}{ifdef_original_term}'
                ifdef_updated.append(ifdef_updated_term)

            tab_depth = tab_depth + 1
        elif line.__contains__('#include "'):
            line = line.replace('#include "', f'#include "{ADB_LOCATION}{FILENAME_PREFIX}')

        text_out += f'{line}\n'

    new_file.write_text(text_out)


def format_write_text_second(file):
    """
    Second pass, to fix up includes and ifdefs
    :param file:
    :return:
    """
    text_in = file.read_text()
    text_in = text_in.splitlines()
    text_out = blank
    changed_flag = False
    for line in text_in:
        for ifdef in ifdef_original:
            if line.__contains__(ifdef) and not line.__contains__(ifdef_updated[ifdef_original.index(ifdef)]):
                changed_flag = True
                line = line.replace(ifdef, ifdef_updated[ifdef_original.index(ifdef)])
        text_out += f'{line}\n'

    # Ghetto iops minimizer
    if changed_flag:
        file.write_text(text_out)


def write_to_unity_folder(path):
    unity_path = Path(str(path).replace(str(paths.target), str(paths.unityAssetsShaders)).replace(r"\\", r"\\"))
    paths.mkdir_ifnexist_bypath(unity_path)
    unity_path.write_text(path.read_text())


# TODO Cleanup and organize loc.
def ensure_exists(old_file, new_file):
    paths.mkdir_ifnexist_bypath(old_file)
    paths.mkdir_ifnexist_bypath(new_file)


def format_filename_target(path):
    base = os.path.dirname(path.replace("\source\\", "\\target\\"))
    path = f'{base}\\{FILENAME_PREFIX}{os.path.basename(path)}'
    return path


# TODO Cleanup and organize loc.
def format_filenames(path):
    return Path(path), Path(format_filename_target(path))


# Holds all ops, because why not.
# Format -  EnumKey: [Pass1Ops,Pass2Ops]
op_dict = {
    EXTENSIONS.CGINC: [
        [ensure_exists, format_write_text_first],
        [format_write_text_second]
    ],
    EXTENSIONS.CS: [
        [],
        []
    ],
    EXTENSIONS.GLSLINC: [
        [],
        []
    ],
    EXTENSIONS.SHADER: [
        [],
        []
    ],
    EXTENSIONS.TXT: [
        [],
        []
    ]
}

if UNITY_TEST_PROJECT_INCLUDED:
    op_dict[EXTENSIONS.CGINC][1].append(write_to_unity_folder)

processed_files_list = {}

# TODO this is stupid. Remind self how to iterate python.
for file_list in file_lists:
    processed_file_list = []
    for file in file_lists[file_list]:
        old_file, new_file = format_filenames(str(file))
        for op in op_dict[file_list][0]:
            op(old_file, new_file)
            processed_file_list.append(new_file)
    processed_files_list[file_list] = processed_file_list

# TODO rework this for better second loop run, to minimize iops. Should we just keep all the text in ram?
for file_list in processed_files_list:
    for file in processed_files_list[file_list]:
        for op in op_dict[file_list][1]:
            op(Path(file))

print(f'Total Duration: {datetime.utcnow() - start_time}')
