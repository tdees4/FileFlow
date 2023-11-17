### FILE WRAPPER CLASS ###

from pathlib import Path
import shutil

class File:
    """
    Represents a file as an object in python
    """
    
    def __init__(self, file_name: str, file_dir: str):
        self.__file_dir = file_dir;
        self.__file_name = file_name
    
    def rename_stem(self, new_name: str):
        file = Path(self.__file_dir)
        file.rename(new_name + file.suffix)
        self.__file_dir = self.__file_dir.replace(self.__file_name, "") + new_name + file.suffix
        self.__file_name = new_name + file.suffix
        
    def move(self, directory: str):
        shutil.move(self.__file_dir, directory)
        self.__file_dir = self.__file_dir.replace(self.__file_name, "") + directory + "\\" + self.__file_name
    
    def get_dir(self) -> str:
        return self.__file_dir
    
    def get_stem(self) -> str:
        return Path(self.__file_dir).stem
    
    def get_suffix(self) -> str:
        return Path(self.__file_dir).suffix
    
    def get_full_name(self) -> str:
        return self.__file_name
    
    def get_parent(self) -> Path:
        return Path(self.__file_dir).parent
    
    def __str__(self) -> str:
        return self.__file_name