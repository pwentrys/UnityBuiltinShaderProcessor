import os
from os.path import realpath, splitext
from pathlib import Path


# DO NOT TOUCH
class Paths:
    def __init__(self, path):
        """
        source defaults to 'source'
        target defaults to 'target'
        """
        # TODO Create actual debugger
        self.log_long = '#---------------------------------------------\n'
        self.log_line = '#\n'
        self.path = realpath(path)
        self.pathOS, self.pathEXT = splitext(self.path)
        self.file = os.path.basename(self.path)
        self.dirOS = str(Path(self.path))
        self.dirOS = self.dirOS.replace(self.file, '')
        self.source = Path(f'{self.dirOS}source')
        self.target = Path(f'{self.dirOS}target')
        self.log = Path(f'{self.pathOS}.log')
        self.create_dependencies()

    @staticmethod
    def mkdir_ifnexist(directory):
        """
        Lazy mkdir extension
        :param directory: 
        :return: 
        """
        if not Path(directory).exists():
            print(f'DIR-Create {directory}')
            os.mkdir(directory)

    def create_dependencies(self):
        """
        Ensure required default folders exist.
        :return: 
        """
        self.mkdir_ifnexist(self.source)
        self.mkdir_ifnexist(self.target)

    def __log__(self):
        """
        Debug log.
        :return: 
        """
        print(
            f'\n{self.log_long}# PATHS - START\n{self.log_long}\n'
            f'Path: {self.path}\n'
            f'PathOS: {self.pathOS}\n'
            f'PathEXT: {self.pathEXT}\n'
            f'DirOS: {self.dirOS}\n'
            f'Source: {self.source}\n'
            f'Target: {self.target}\n'
            f'Log: {self.log}\n'
            f'\n{self.log_long}# PATHS - END\n{self.log_long}\n'
        )
