import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox, simpledialog
import os
import platform

class NotesApp(ctk.CTk):
    """
    A modern, professional notes application built with CustomTkinter.
    It features a responsive layout, light/dark mode, and file-based note storage.
    """
    def __init__(self):
        super().__init__()

        # --- APP CONFIGURATION ---
        self.title("Notes App")
        self.geometry("1000x600")
        self.minsize(700, 450)

        # --- CLASS VARIABLES ---
        self.notes_directory = "notes"  # Directory to store note files
        self.current_note_file = None   # Path to the currently opened note file
        self.note_widgets = {}          # Dictionary to keep track of note list widgets

        # --- INITIAL SETUP ---
        self._setup_notes_directory()
        self._create_widgets()
        self._load_notes_into_sidebar()

        # --- WINDOW PROTOCOLS ---
        # Set a handler for the window close event
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_widgets(self):
        """Creates and configures all UI widgets for the application."""

        # --- LAYOUT CONFIGURATION ---
        # Configure the main grid layout (1 row, 2 columns)
        self.grid_rowconfigure(0, weight=1)
        # Sidebar (column 0) has a fixed width, Main content (column 1) expands
        self.grid_columnconfigure(0, weight=0, minsize=250)
        self.grid_columnconfigure(1, weight=1)

        # --- SIDEBAR (LEFT FRAME) ---
        self.sidebar_frame = ctk.CTkFrame(self, width=250, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(3, weight=1) # Make the notes list expandable

        # App Title Label
        app_title_label = ctk.CTkLabel(self.sidebar_frame, text="Notes App", font=ctk.CTkFont(size=20, weight="bold"))
        app_title_label.grid(row=0, column=0, columnspan=2, padx=20, pady=(20, 10))

        # New Note Button
        self.new_note_button = ctk.CTkButton(self.sidebar_frame, text="New Note", command=self._new_note)
        self.new_note_button.grid(row=1, column=0, padx=(20, 10), pady=10, sticky="ew")

        # Delete Note Button
        self.delete_note_button = ctk.CTkButton(self.sidebar_frame, text="Delete Note", command=self._delete_note, fg_color="#D32F2F", hover_color="#B71C1C")
        self.delete_note_button.grid(row=1, column=1, padx=(10, 20), pady=10, sticky="ew")

        # Search Bar
        self.search_entry = ctk.CTkEntry(self.sidebar_frame, placeholder_text="Search notes...")
        self.search_entry.grid(row=2, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="ew")
        self.search_entry.bind("<KeyRelease>", self._filter_notes)

        # Scrollable Frame for Notes List
        self.notes_list_frame = ctk.CTkScrollableFrame(self.sidebar_frame, label_text="My Notes")
        self.notes_list_frame.grid(row=3, column=0, columnspan=2, padx=20, pady=(0, 10), sticky="nsew")

        # Theme Switcher
        self.theme_label = ctk.CTkLabel(self.sidebar_frame, text="Theme:")
        self.theme_label.grid(row=4, column=0, columnspan=2, padx=20, pady=(0, 5), sticky="w")
        self.theme_switch = ctk.CTkSegmentedButton(self.sidebar_frame, values=["Light", "Dark", "System"], command=self._change_theme)
        self.theme_switch.set("System") # Default value
        self.theme_switch.grid(row=5, column=0, columnspan=2, padx=20, pady=(0, 20), sticky="ew")

        # --- MAIN CONTENT AREA (RIGHT FRAME) ---
        self.main_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.main_frame.grid(row=0, column=1, sticky="nsew", padx=20, pady=20)
        self.main_frame.grid_rowconfigure(1, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Note Title Entry
        self.title_entry = ctk.CTkEntry(self.main_frame, placeholder_text="Enter note title here...", font=ctk.CTkFont(size=18))
        self.title_entry.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        # Note Content Textbox
        self.content_textbox = ctk.CTkTextbox(self.main_frame, font=ctk.CTkFont(size=14), wrap="word")
        self.content_textbox.grid(row=1, column=0, columnspan=2, sticky="nsew")

        # Save Button
        self.save_button = ctk.CTkButton(self.main_frame, text="Save Note", command=self._save_note)
        self.save_button.grid(row=2, column=0, sticky="e", pady=(10, 0))
        
        # Initially disable editing fields until a note is selected or created
        self._set_editor_state("disabled")


    # --- CORE FUNCTIONALITY ---

    def _setup_notes_directory(self):
        """Checks for the notes directory and creates it if it doesn't exist."""
        try:
            if not os.path.exists(self.notes_directory):
                os.makedirs(self.notes_directory)
        except OSError as e:
            messagebox.showerror("Error", f"Failed to create notes directory:\n{e}")
            self.quit()

    def _load_notes_into_sidebar(self):
        """Scans the notes directory and populates the sidebar with note buttons."""
        # Clear existing note widgets
        for widget in self.note_widgets.values():
            widget.destroy()
        self.note_widgets = {}

        try:
            # Sort files by modification time, newest first
            files = sorted(
                [f for f in os.listdir(self.notes_directory) if f.endswith(".txt")],
                key=lambda f: os.path.getmtime(os.path.join(self.notes_directory, f)),
                reverse=True
            )
            
            for filename in files:
                note_title = os.path.splitext(filename)[0]
                filepath = os.path.join(self.notes_directory, filename)
                
                # Create a button for each note
                note_button = ctk.CTkButton(
                    self.notes_list_frame,
                    text=note_title,
                    fg_color="transparent",
                    anchor="w",
                    command=lambda fp=filepath, title=note_title: self._select_note(fp, title)
                )
                note_button.pack(fill="x", padx=5, pady=2)
                self.note_widgets[filepath] = note_button

        except OSError as e:
            messagebox.showerror("Error", f"Failed to load notes:\n{e}")

    def _select_note(self, filepath, title):
        """Loads the content of a selected note into the editor."""
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()

            # Clear current editor content
            self.title_entry.delete(0, "end")
            self.content_textbox.delete("1.0", "end")

            # Insert new content
            self.title_entry.insert(0, title)
            self.content_textbox.insert("1.0", content)

            self.current_note_file = filepath
            self._highlight_selected_note(filepath)
            self._set_editor_state("normal")

        except FileNotFoundError:
            messagebox.showwarning("Warning", "The selected note file was not found. It may have been deleted.")
            self._load_notes_into_sidebar() # Refresh the list
            self._clear_editor()
        except Exception as e:
            messagebox.showerror("Error", f"An error occurred while opening the note:\n{e}")

    def _new_note(self):
        """Clears the editor to start a new note."""
        self._clear_editor()
        self.current_note_file = None
        self._highlight_selected_note(None) # Un-highlight all notes
        self._set_editor_state("normal")
        self.title_entry.focus()
        
    def _save_note(self):
        """Saves the current note (new or existing) to a text file."""
        title = self.title_entry.get().strip()
        content = self.content_textbox.get("1.0", "end-1c").strip()

        if not title:
            messagebox.showwarning("Warning", "Please enter a title for the note.")
            return

        # Sanitize title to create a valid filename
        # This replaces spaces with underscores and removes invalid characters
        sanitized_title = "".join(c for c in title if c.isalnum() or c in " ._").rstrip()
        if not sanitized_title:
             messagebox.showwarning("Warning", "Title contains only invalid characters for a filename.")
             return

        new_filepath = os.path.join(self.notes_directory, f"{sanitized_title}.txt")

        # Handle renaming or overwriting conflicts
        if self.current_note_file and self.current_note_file != new_filepath and os.path.exists(new_filepath):
             if not messagebox.askyesno("Confirm Overwrite", f"A note named '{sanitized_title}' already exists. Do you want to overwrite it?"):
                 return
        elif not self.current_note_file and os.path.exists(new_filepath):
            if not messagebox.askyesno("Confirm Overwrite", f"A note named '{sanitized_title}' already exists. Do you want to overwrite it?"):
                 return

        try:
            # If it's a renamed note, delete the old file
            if self.current_note_file and self.current_note_file != new_filepath:
                os.remove(self.current_note_file)
            
            # Write the new/updated file
            with open(new_filepath, 'w', encoding='utf-8') as f:
                f.write(content)

            self.current_note_file = new_filepath
            messagebox.showinfo("Success", f"Note '{title}' saved successfully.")
            self._load_notes_into_sidebar() # Refresh to show new/renamed note and correct order
            self._highlight_selected_note(new_filepath)
        
        except OSError as e:
            messagebox.showerror("Error", f"Failed to save note:\n{e}")
        except Exception as e:
            messagebox.showerror("Error", f"An unexpected error occurred:\n{e}")

    def _delete_note(self):
        """Deletes the currently selected note."""
        if not self.current_note_file:
            messagebox.showwarning("Warning", "No note is selected to delete.")
            return

        title = os.path.splitext(os.path.basename(self.current_note_file))[0]
        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to permanently delete the note '{title}'?"):
            try:
                os.remove(self.current_note_file)
                self.current_note_file = None
                self._clear_editor()
                self._set_editor_state("disabled")
                self._load_notes_into_sidebar() # Refresh list
                messagebox.showinfo("Success", "Note deleted.")
            except FileNotFoundError:
                messagebox.showwarning("Warning", "The note file was not found. It may have already been deleted.")
                self._load_notes_into_sidebar() # Refresh the list
            except OSError as e:
                messagebox.showerror("Error", f"Failed to delete note:\n{e}")
    
    # --- UI HELPERS AND EVENT HANDLERS ---
    
    def _clear_editor(self):
        """Clears all text from the title and content fields."""
        self.title_entry.delete(0, "end")
        self.content_textbox.delete("1.0", "end")
        self.current_note_file = None

    def _set_editor_state(self, state):
        """Enables or disables the main editor widgets."""
        self.title_entry.configure(state=state)
        self.content_textbox.configure(state=state)
        self.save_button.configure(state=state)

    def _highlight_selected_note(self, selected_filepath):
        """Changes the appearance of the selected note in the sidebar."""
        for filepath, button in self.note_widgets.items():
            if filepath == selected_filepath:
                button.configure(fg_color=("gray75", "gray25")) # Highlight color
            else:
                button.configure(fg_color="transparent") # Default color

    def _filter_notes(self, event=None):
        """Filters the notes in the sidebar based on the search entry text."""
        search_term = self.search_entry.get().lower()
        for filepath, button in self.note_widgets.items():
            note_title = os.path.splitext(os.path.basename(filepath))[0]
            if search_term in note_title.lower():
                button.pack(fill="x", padx=5, pady=2) # Show
            else:
                button.pack_forget() # Hide

    def _change_theme(self, new_theme):
        """Changes the application's appearance mode."""
        ctk.set_appearance_mode(new_theme)
    
    def _on_closing(self):
        """Handles the window close event. Will eventually check for unsaved changes."""
        # This is a placeholder for future functionality like checking for unsaved changes.
        # For now, it just closes the app.
        self.destroy()

def main():
    """The main function to set up and run the application."""
    # Set default appearance and color theme
    ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Options: "blue", "green", "dark-blue"

    app = NotesApp()
    app.mainloop()

if __name__ == "__main__":
    main()