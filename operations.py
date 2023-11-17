### HANDLES ALL FILE OPERATIONS ###

from pathlib import Path
from file import File

def to_file_objects(files: list[str], directory: str) -> list:
    output = []
    for file in files:
        file_obj = File(file, directory + "\\" + file)
        output.append(file_obj)
    return output

def rename_files(files: list, new_name: str):
    for file in files:
        file.rename_stem(new_name)

def combine_files(files: list, folder_name: str):
    Path(folder_name).mkdir(exist_ok=True)
    move_files(files, folder_name)
    
def move_files(files: list, folder: str):
    for file in files:
        file.move(folder)

def remove_characters_from_file_names(files: list, characters: list[str]):
    for file in files:
        name = file.get_stem()
        
        for character in characters:
            while name.find(character) >= 0:
                name = name.replace(character, "")
        
        file.rename_stem(name)

def append_parent_folder_name(files: list):
    for file in files:
        new_name = file.get_parent().stem + "" +  file.get_stem()
        file.rename_stem(new_name)