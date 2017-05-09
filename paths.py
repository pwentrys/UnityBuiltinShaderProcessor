import os
from os.path import realpath, splitext
from pathlib import Path

from config import UNITY_TEST_PROJECT_INCLUDED


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
        self.unity = Path(f'{self.dirOS}unity')
        self.unityAssets = Path(f'{self.unity}\\Assets')
        self.unityAssetsShaders = Path(f'{self.unityAssets}\\Shaders')
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
            try:
                # TODO ...Totally no way this could ever go wrong /s
                parent = Path(os.path.normpath(f'{str(directory)}\\..\\'))
                if not parent.exists():
                    parent.mkdir()

                os.mkdir(directory)
            except Exception as e:
                print(e)

    @staticmethod
    def mkdir_ifnexist_bypath(path):
        """
        Mkdir using path
        :param path: 
        :return: 
        """
        filename = os.path.basename(path)
        directory = str(Path(path))
        Paths.mkdir_ifnexist(directory.replace(filename, ''))

    def create_dependencies(self):
        """
        Ensure required default folders exist.
        :return: 
        """
        self.mkdir_ifnexist(self.source)
        self.mkdir_ifnexist(self.target)
        if UNITY_TEST_PROJECT_INCLUDED:
            self.mkdir_ifnexist(self.unity)
            self.mkdir_ifnexist(self.unityAssets)
            self.mkdir_ifnexist(self.unityAssetsShaders)

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
            f'Unity: {self.unity}\n'
            f'UnityAssets: {self.unityAssets}\n'
            f'UnityAssetsShaders: {self.unityAssetsShaders}\n'
            f'Log: {self.log}\n'
            f'\n{self.log_long}# PATHS - END\n{self.log_long}\n'
        )
