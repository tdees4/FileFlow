### HOLDS THE CLASSES FOR ALL FILE OPERATION BUTTONS ###

import customtkinter as ctk
import operations

class OperationButton(ctk.CTkButton):
    """
    The base class for the buttons that handle
    file operations in the FileFlow GUI. Requires child classes
    to implement on_left_click
    """
    def __init__(self, parent_app, place_x, place_y, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_app = parent_app
        self.bind(
            "<Button-1>",
            command = self.on_left_click
        )
        self.place(
            x = place_x,
            y = place_y
        )
        
    def on_left_click(self, *args):
        """
        Handles the logic that takes place when the button is
        left clicked
        """
        raise NotImplementedError("Please implement this method!")

class RenameButton(OperationButton):
    def __init__(self, parent_app, master, **kwargs):
        super().__init__(parent_app=parent_app, place_x=75, place_y=400, master=master, **kwargs)
        
    def on_left_click(self, *args):
        dialog = ctk.CTkInputDialog(
            title = "",
            text = "Enter a new name to give to the selected files"
        )
        try:
            operations.rename_files(
                operations.to_file_objects(self.parent_app._get_selected_files(), self.parent_app._get_directory()),
                dialog.get_input()
            )
        except:
            print("Could not complete rename function.")
        self.parent_app.list_frame.populate(self.parent_app._get_directory_files())
        
class CombineButton(OperationButton):
    def __init__(self, parent_app, master, **kwargs):
        super().__init__(parent_app=parent_app, place_x=142, place_y=400, master=master, **kwargs)
        
    def on_left_click(self, *args):
        dialog = ctk.CTkInputDialog(
            title = "",
            text = "Enter a name for the folder"
        )
        
        try:
            operations.combine_files(
                operations.to_file_objects(self.parent_app._get_selected_files(), self.parent_app._get_directory()),
                dialog.get_input()
            )
        except:
            print("Could not complete combine function")
        self.parent_app.list_frame.populate(self.parent_app._get_directory_files())
        
class MoveButton(OperationButton):
    def __init__(self, parent_app, master, **kwargs):
        super().__init__(parent_app=parent_app, place_x=214, place_y=400, master=master, **kwargs)
    
    def on_left_click(self, *args):
        dialog = ctk.CTkInputDialog(
            title = "",
            text = "Enter the directory to move the files to"
        )
        try:
            operations.move_files(
                    operations.to_file_objects(self.parent_app._get_selected_files(), self.parent_app._get_directory()),
                    dialog.get_input()
                )
        except:
            print("Could not complete move function")
        self.parent_app.list_frame.populate(self.parent_app._get_directory_files())
        
class RemoveCharactersButton(OperationButton):
    def __init__(self, parent_app, master, **kwargs):
        super().__init__(parent_app=parent_app, place_x=265, place_y=400, master=master, **kwargs)
        
    def on_left_click(self, *args):
        dialog = ctk.CTkInputDialog(
            title = "",
            text = "Enter the characters you want to remove with each separated by a comma"
        )
        try:
            operations.remove_characters_from_file_names(
                operations.to_file_objects(self.parent_app._get_selected_files(), self.parent_app._get_directory()),
                dialog.get_input().split(",")
            )
        except:
            print("Could not complete character remove function")
        self.parent_app.list_frame.populate(self.parent_app._get_directory_files())
        
class AppendParentNameButton(OperationButton):
    def __init__(self, parent_app, master, **kwargs):
        super().__init__(parent_app=parent_app, place_x=413, place_y=400, master=master, **kwargs)
        
    def on_left_click(self, *args):
        try:
            operations.append_parent_folder_name(
                operations.to_file_objects(self.parent_app._get_selected_files(), self.parent_app._get_directory())
            )
        except:
            print("Could not complete append parent name function")
        self.parent_app.list_frame.populate(self.parent_app._get_directory_files())
        