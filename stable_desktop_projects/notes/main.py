import customtkinter as ctk
import tkinter as tk
from tkinter import filedialog, messagebox
import os

# --- Main Application Class ---
class NotesApp(ctk.CTk):
    """
    A modern desktop notes application built with CustomTkinter.
    It allows users to create, save, open, and delete text-based notes.
    """
    def __init__(self):
        super().__init__()

        # --- Window Configuration ---
        self.title("Notes")
        self.geometry("900x600")
        self.minsize(600, 400)

        # --- App State Variables ---
        self.notes_directory = "notes_data"
        self.current_file_path = None
        self.text_modified = False  # Flag to track unsaved changes

        # --- Initialize UI ---
        self._setup_layout()
        self._create_widgets()
        self._load_notes()
        
        # --- Window Closing Protocol ---
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _setup_layout(self):
        """
        Configures the main window's grid layout for responsiveness.
        The layout consists of a sidebar (column 0) and a main content area (column 1).
        """
        self.grid_columnconfigure(1, weight=1)
        self.grid_rowconfigure(0, weight=1)

    def _create_widgets(self):
        """Creates and places all the UI widgets in the window."""

        # --- Sidebar Frame (Left) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nswe")
        self.sidebar_frame.grid_rowconfigure(2, weight=1)

        # Sidebar Title
        self.sidebar_title_label = ctk.CTkLabel(self.sidebar_frame, text="My Notes", font=ctk.CTkFont(size=20, weight="bold"))
        self.sidebar_title_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # "New Note" Button
        self.new_note_button = ctk.CTkButton(self.sidebar_frame, text="New Note", command=self._new_note)
        self.new_note_button.grid(row=1, column=0, padx=20, pady=10)

        # Scrollable frame for notes list
        self.notes_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="Files")
        self.notes_list_frame.grid(row=2, column=0, padx=20, pady=10, sticky="nsew")

        # Theme Switcher
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:")
        self.theme_label.grid(row=3, column=0, padx=20, pady=(10, 0), sticky="sw")
        self.theme_switch = ctk.CTkSwitch(self.sidebar_frame, text="Dark", command=self._toggle_theme, onvalue="Dark", offvalue="Light")
        self.theme_switch.grid(row=4, column=0, padx=20, pady=(5, 20), sticky="sw")
        self.theme_switch.select() # Start in dark mode by default

        # --- Main Content Frame (Right) ---
        self.main_frame = ctk.CTkFrame(self, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, padx=20, pady=20, sticky="nsew")
        self.main_frame.grid_columnconfigure(0, weight=1)
        self.main_frame.grid_rowconfigure(2, weight=1)

        # Toolbar for Save/Delete buttons
        self.toolbar_frame = ctk.CTkFrame(self.main_frame)
        self.toolbar_frame.grid(row=0, column=0, sticky="ew", pady=(0,10))
        self.toolbar_frame.grid_columnconfigure(2, weight=1)

        self.save_button = ctk.CTkButton(self.toolbar_frame, text="Save Note", command=self._save_note)
        self.save_button.grid(row=0, column=0, padx=(0, 10))
        
        self.delete_button = ctk.CTkButton(self.toolbar_frame, text="Delete Note", command=self._delete_note, fg_color="#D32F2F", hover_color="#B71C1C")
        self.delete_button.grid(row=0, column=1)

        # Title Entry
        self.title_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter note title here...", font=ctk.CTkFont(size=16, weight="bold"))
        self.title_entry.grid(row=1, column=0, sticky="ew", pady=(0, 10))

        # Text Editor
        self.text_editor = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=14), wrap="word")
        self.text_editor.grid(row=2, column=0, sticky="nsew")
        
        # Bind text modification event
        self.text_editor.bind("<KeyRelease>", self._on_text_modified)
        self.title_entry.bind("<KeyRelease>", self._on_text_modified)

    # --- Event Handlers and Functionality ---

    def _on_text_modified(self, event=None):
        """Sets the text_modified flag to True when text is changed."""
        self.text_modified = True

    def _toggle_theme(self):
        """Switches the application theme between 'Dark' and 'Light'."""
        mode = self.theme_switch.get()
        ctk.set_appearance_mode(mode)

    def _check_unsaved_changes(self):
        """
        Checks for unsaved changes and prompts the user to save.
        Returns False if the user cancels the action, True otherwise.
        """
        if self.text_modified:
            response = messagebox.askyesnocancel("Unsaved Changes", "You have unsaved changes. Do you want to save them before continuing?")
            if response is True:  # Yes
                self._save_note()
                return not self.text_modified # Return True if save was successful
            elif response is False:  # No
                return True # Proceed without saving
            else:  # Cancel
                return False # Abort the current action
        return True # No changes, proceed

    def _load_notes(self):
        """
        Loads notes from the notes directory and populates the sidebar.
        Creates the directory if it doesn't exist.
        """
        # Create directory if it doesn't exist
        if not os.path.exists(self.notes_directory):
            try:
                os.makedirs(self.notes_directory)
            except OSError as e:
                messagebox.showerror("Error", f"Failed to create notes directory:\n{e}")
                return

        # Clear existing notes from the list
        for widget in self.notes_list_frame.winfo_children():
            widget.destroy()

        # Load notes from files
        try:
            files = [f for f in os.listdir(self.notes_directory) if f.endswith(".txt")]
            for filename in sorted(files, key=str.lower):
                file_path = os.path.join(self.notes_directory, filename)
                # Display name without the .txt extension
                display_name = os.path.splitext(filename)[0]
                
                note_button = ctk.CTkButton(self.notes_list_frame, text=display_name,
                                            command=lambda p=file_path: self._open_note(p),
                                            fg_color="transparent", anchor="w")
                note_button.pack(fill="x", padx=5, pady=2)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to read notes from directory:\n{e}")
            
    def _new_note(self):
        """Clears the editor to start a new note."""
        if not self._check_unsaved_changes():
            return
            
        self.title_entry.delete(0, tk.END)
        self.text_editor.delete("1.0", tk.END)
        self.current_file_path = None
        self.text_modified = False
        self.title_entry.focus()
        messagebox.showinfo("Information", "New note created. Enter a title and start typing.")

    def _open_note(self, file_path):
        """Opens a selected note file and displays its content."""
        if not self._check_unsaved_changes():
            return
            
        try:
            with open(file_path, 'r', encoding='utf-8') as file:
                # First line is the title, the rest is content
                title = file.readline().strip()
                content = file.read()

                self.title_entry.delete(0, tk.END)
                self.title_entry.insert(0, title)

                self.text_editor.delete("1.0", tk.END)
                self.text_editor.insert("1.0", content)

                self.current_file_path = file_path
                self.text_modified = False
        except FileNotFoundError:
            messagebox.showerror("Error", "The note file was not found.")
            self._load_notes() # Refresh list if file was deleted externally
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open note:\n{e}")

    def _save_note(self):
        """Saves the current note to a file."""
        title = self.title_entry.get().strip()
        content = self.text_editor.get("1.0", tk.END).strip()

        if not title:
            messagebox.showwarning("Warning", "Please enter a title for the note.")
            return

        # Sanitize filename
        filename = "".join([c for c in title if c.isalnum() or c in (' ', '_')]).rstrip()
        filename = f"{filename}.txt"
        
        # Use current path if it exists, otherwise create a new one
        save_path = self.current_file_path if self.current_file_path else os.path.join(self.notes_directory, filename)

        try:
            with open(save_path, 'w', encoding='utf-8') as file:
                file.write(title + '\n')
                file.write(content)
            
            self.current_file_path = save_path
            self.text_modified = False
            messagebox.showinfo("Success", f"Note '{title}' saved successfully.")
            self._load_notes() # Refresh list to show new or renamed note
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save note:\n{e}")

    def _delete_note(self):
        """Deletes the currently opened note."""
        if not self.current_file_path:
            messagebox.showwarning("Warning", "No note is currently open to delete.")
            return

        title = self.title_entry.get()
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete the note '{title}'?"):
            try:
                os.remove(self.current_file_path)
                messagebox.showinfo("Success", f"Note '{title}' has been deleted.")
                self._new_note() # Clear the fields
                self._load_notes() # Refresh the list
            except FileNotFoundError:
                messagebox.showerror("Error", "File not found. It may have already been deleted.")
                self._load_notes() # Refresh list
            except Exception as e:
                messagebox.showerror("Error", f"Failed to delete note:\n{e}")

    def _on_closing(self):
        """Handles the window closing event."""
        if self._check_unsaved_changes():
            self.destroy()

# --- Main Function and Entry Point ---
def main():
    """Main function to initialize and run the application."""
    # Set initial theme. "System" will adapt to the OS setting.
    ctk.set_appearance_mode("Dark") 
    # Set default color theme for widgets.
    ctk.set_default_color_theme("blue") 
    
    app = NotesApp()
    app.mainloop()

if __name__ == "__main__":
    main()