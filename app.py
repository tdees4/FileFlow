### HANDLES THE GUI ###

import customtkinter as ctk
from file import File
from operation_buttons import *

WINDOW_X = 700
WINDOW_Y = 450

class App(ctk.CTk):
    """
    Represents the main window for the FileFlow program and contains all
    GUI elements
    """
    
    def __init__(self, os):
        super().__init__()
        
        self.title("FileFlow App")
        self.geometry(str(700) + "x" + str(450))
        self.minsize(700, 450)
        self.maxsize(700, 450)
        
        self.__selected_files = []
        self.__os = os
        
        self.__display_directory()
        
        self.mainloop()
        
    def select_file(self, file_name: str) -> bool:
        """
        Handles file selection logic. If the selected file is already in the
        selected list, it removes the file from the list. Otherwise, the selected
        file is simply added to the selected files list. Updates the GoTo button after
        each selection.
        
        Returns:
            bool: Returns True if the file being selected is not in the selected files
            list, False otherwise
        """
        if (self.__selected_files.count(file_name) > 0):
            self.__selected_files.remove(file_name)
            self.goto_button.update_button(self.__selected_files)
            return False
        else:
            self.__selected_files.append(file_name)
            self.goto_button.update_button(self.__selected_files)
            return True
        
    def change_directory(self, directory: str):
        """
        Handles the changing of the current directory and updates all
        necessary GUI elements upon changing the directory
        """
        self.__os.chdir(directory)
        self.clear_selected_files()
       
        if self.list_frame != None:
           self.list_frame.populate(self._get_directory_files())
        if self.directory_text != None:
            self.directory_text.configure(text = directory)
        if self.goto_button != None:
            self.goto_button.update_button(self.__selected_files)
       
    def clear_selected_files(self):
        self.__selected_files.clear()
        
    def _get_directory_files(self) -> list[File]:
        """
        Iterates through all of the files in the current directory and
        returns them as a list of File objects
        """
        output_list = []
        
        for file in self.__os.listdir():
            output_list.append(File(file, self.__os.getcwd() + "\\" + file))
            
        return output_list
    
    def _get_selected_files(self) -> list[str]:
        return self.__selected_files

    def _get_directory(self) -> str:
        return self.__os.getcwd()
            
    
    def __display_directory(self):
        self.directory_text = ctk.CTkLabel(
            master = self,
            text = self.__os.getcwd()
        )
        self.directory_text.pack()
        
        self.list_frame = FileListFrame(
            parent_app = self,
            master = self,
            width = 650,
            height = 350,
            fg_color = "#3f4045"
        )
        self.list_frame.populate(self._get_directory_files())
        
        self.back_button = BackButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "BACK"
        )
        
        self.goto_button = GoToButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "GO TO"
        )
        
        self.rename_button = RenameButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "RENAME"
        )
        
        self.combine_button = CombineButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "COMBINE"
        )
        
        self.move_button = MoveButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "MOVE"
        )
        
        self.character_remove_button = RemoveCharactersButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "REMOVE CHARACTERS"
        )
        
        self.append_parent_name = AppendParentNameButton(
            parent_app = self,
            master = self,
            width = 45,
            height = 20,
            text = "APPEND PARENT NAME"
        )
        

class FileListFrame(ctk.CTkScrollableFrame):
    """
    Represents the frame that holds all of the directory's files and
    folders as buttons.
    """
    
    def __init__(self, parent_app: App, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_app = parent_app
        self.__file_buttons = []
        self.pack()
        
    def populate(self, file_list: list[File]):
        """
        Clears all current file buttons from the frame and repopulates
        the frame with the current directory's files. Best to use this when
        refreshing the file list after making a change or changing the directory.
        """
        self.clear_widgets()
        
        for file in file_list:
            button = FileButton(
                index = len(self.__file_buttons),
                parent_app = self.parent_app,
                master = self,
                text = file.get_full_name(),
                width = self.cget("width"),
                height = 35,
                corner_radius = 0
            )
            
            self.__file_buttons.append(button)
            
    
    def unhighlight_buttons(self):
        for button in self.__file_buttons:
            button.unhighlight()
    
    def clear_widgets(self):
        for widget in self.__file_buttons:
            widget.destroy()
        self.__file_buttons.clear()
        
            
class FileButton(ctk.CTkButton):
    """
    Represents a file in the current directory as a button that
    can be selected
    """
    
    def __init__(self, index, parent_app: App, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_app = parent_app
        self.__main_color = self.cget("fg_color")
        self.bind(
            "<Button-1>",
            command = self.on_left_click
        )
        self.bind(
            "<Shift-Button-1>",
            command = self.on_shift_left_click
        )
        self.grid(
            row = index,
            column = 0
        )
        
    def on_left_click(self, *args): # Select one file at a time #
        self.parent_app.clear_selected_files()
        self.parent_app.list_frame.unhighlight_buttons()
        self.parent_app.select_file(self.cget("text"))
        self.highlight()
        
    def on_shift_left_click(self, *args): # Select multiple files at a time #
        if self.parent_app.select_file(self.cget("text")):
            self.highlight()
        else:
            self.unhighlight()
        
    def highlight(self):
        self.configure(fg_color = self.cget("hover_color"))
        
    def unhighlight(self):
        self.configure(fg_color = self.__main_color)
       
        
class BackButton(ctk.CTkButton):
    """
    Represents a button that allows the user to navigate back to the
    parent directory
    """
    
    def __init__(self, parent_app: App, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_app = parent_app
        self.bind(
            "<Button-1>",
            command = self.on_left_click
        )
        self.place(
            x = 20,
            y = 5
        )
    
    def on_left_click(self, *args):
        self.parent_app.change_directory(
            self.parent_app._get_directory()[:self.parent_app._get_directory().rfind("\\")]
        )


class GoToButton(ctk.CTkButton):
    """
    Represents a button that allows the user to navigate to the
    selected folder. This button only works if a folder is selected.
    """
    
    def __init__(self, parent_app: App, master, **kwargs):
        super().__init__(master, **kwargs)
        self.parent_app = parent_app
        self.__main_color = self.cget("fg_color")
        self.__folder = ""
        self.unhighlight()
        self.bind(
            "<Button-1>",
            command = self.on_left_click
        )
        self.place(
            x = 20,
            y = 400
        )
        
    def update_button(self, selected_files: list[str]):
        """
        The button is only highlighted when a single file is selected and
        that file is a folder. The button being highlighted is meant to
        show that it can be used.
        """
        if (len(selected_files) == 0 or len(selected_files) > 1):
            self.unhighlight()
            self.__folder = ""
        elif (selected_files[0].count(".") == 0):
            self.highlight()
            self.__folder = selected_files[0]
        else:
            self.unhighlight()
            
    def on_left_click(self, *args):
        self.parent_app.change_directory(
            self.parent_app._get_directory() + "\\" + self.__folder
        )
        
    def highlight(self):
        self.configure(fg_color = self.cget("hover_color"))
        
    def unhighlight(self):
        self.configure(fg_color = self.__main_color)