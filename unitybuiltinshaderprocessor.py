import os
from datetime import datetime
from pathlib import Path

import enums.exts as ext_enum
from config import ADB_CGINCLUDES_LOCATION, FILENAME_BLACKLIST, FILENAME_PREFIX
from enums.contains_terms import CONTAINS_TERMS
from enums.exts import EXTENSIONS
from paths import Paths

start_time = datetime.utcnow()

paths = Paths(__file__)
# paths.__log__()

source = paths.source
GLOBAL_FLAG = EXTENSIONS.TXT

# TODO organize loc.
space = ' '
blank = ''
ifdef_original = []
ifdef_updated = []
processed_files_list = {}

# TODO organize loc.
contains_terms_dict = {
    CONTAINS_TERMS.SPACE: ['defined', space, '#'],
    CONTAINS_TERMS.DEPTH_DECREASE: [r'#el', r'#end', r'}'],
    CONTAINS_TERMS.DEPTH_INCREASE: [r'#if', r'#el', r'{']
}
file_lists = {}

# Force the map to exist
for EXTENSION in EXTENSIONS:
    file_lists[EXTENSION] = []

# Map / sort all the files.
for root, dirnames, filenames in os.walk(str(source)):
    for filename in filenames:
        if not FILENAME_BLACKLIST.__contains__(filename):
            file = Path(f'{root}\\{filename}')
            file_lists[ext_enum.get_type_from_path(file)].append(file)


def do_blank(args):
    """
    This is where the magic doesn't happen.
    :param args:
    :return:
    """
    return args


pass_first = do_blank
pass_second = do_blank


# TODO Find cozy home.
def contains_term_from_list(name, terms):
    """
    Iter check for term
    :param name:
    :param terms:
    :return:
    """
    for term in terms:
        if name.__contains__(term):
            return True
    return False


def format_write_cs_first(args):
    """
    [line, tab_depth, first_ifdef_recorded]
    :param args:
    :return:
    """
    class_name_changed = args[2]
    if class_name_changed:
        return args

    line = args[0]

    if line.__contains__('StandardShaderGUI'):
        line = line.replace('StandardShaderGUI', f'{FILENAME_PREFIX}StandardShaderGUI')
        class_name_changed = True
    tab_depth = args[1]
    return [line, tab_depth, class_name_changed]


def format_write_cginc_first(args):
    """
    [line, tab_depth, first_ifdef_recorded]
    :param args:
    :return:
    """
    line = args[0]
    tab_depth = args[1]
    first_ifdef_recorded = args[2]
    if line.__contains__('CustomEditor "StandardShaderGUI"'):
        line = line.replace('CustomEditor "StandardShaderGUI"', f'CustomEditor "{FILENAME_PREFIX}StandardShaderGUI"')
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
    elif line.__contains__('#include "') and not contains_term_from_list(line, FILENAME_BLACKLIST):
        line = line.replace('#include "', f'#include "{ADB_CGINCLUDES_LOCATION}{FILENAME_PREFIX}')
    # TODO Move this. Being lazy.
    elif not first_ifdef_recorded and line.__contains__('Shader "') and not line.__contains__('Shader "Hidden'):
        line = line.replace('Shader "', 'Shader "Blasto/')

    return [line, tab_depth, first_ifdef_recorded]


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
    first_ifdef_recorded = False
    text_out = blank
    args = ["", tab_depth, first_ifdef_recorded]
    op = define_passes(GLOBAL_FLAG)
    for line in lines:
        args[0] = line
        args = op(args)
        text_out += f'{args[0]}\n'

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


def define_passes(ext_val):
    """
    Overwrite function based depending on enum flag.
    :param ext_val:
    :return:
    """
    if ext_val in [EXTENSIONS.CGINC, EXTENSIONS.GLSLINC, EXTENSIONS.SHADER]:
        return format_write_cginc_first
    elif ext_val in [EXTENSIONS.CS]:
        return format_write_cs_first
    else:
        return do_blank


def write_to_unity_folder(path):
    """
    Writes text file to specified unity folder.
    :param path:
    :return:
    """
    unity_path = Path(str(path).replace(str(paths.target), str(paths.unityAssetsShaders)))
    paths.mkdir_ifnexist_bypath(unity_path)
    unity_path.write_text(path.read_text())


def ensure_exists(old_file, new_file):
    """
    Ensure existence of files
    :param old_file:
    :param new_file:
    :return:
    """
    paths.mkdir_ifnexist_bypath(old_file)
    paths.mkdir_ifnexist_bypath(new_file)


def format_filename_target(path):
    """
    Swaps /source/ to /target/ + extra formatting.
    :param path:
    :return:
    """
    base = os.path.dirname(path.replace("\source\\", "\\target\\"))
    # TODO Better this.
    if GLOBAL_FLAG is EXTENSIONS.TXT:
        return f'{base}\\{os.path.basename(path)}'
    else:
        return f'{base}\\{FILENAME_PREFIX}{os.path.basename(path)}'


# TODO Cleanup and organize loc.
def format_filenames(path):
    """
    Lazy bridge.
    :param path:
    :return:
    """
    return Path(path), Path(format_filename_target(path))


# Two passed run at this point. First pass formats and records data, second pass improves references and saves.
for file_list in file_lists:
    GLOBAL_FLAG = file_list
    processed_file_list = []
    for file in file_lists[file_list]:
        old_file, new_file = format_filenames(str(file))
        ensure_exists(old_file, new_file)
        format_write_text_first(old_file, new_file)
        processed_file_list.append(new_file)
    processed_files_list[file_list] = processed_file_list

for file_list in processed_files_list:
    GLOBAL_FLAG = file_list
    for file in processed_files_list[file_list]:
        format_write_text_second(Path(file))
        write_to_unity_folder(Path(file))

print(f'Total Duration: {datetime.utcnow() - start_time}')
