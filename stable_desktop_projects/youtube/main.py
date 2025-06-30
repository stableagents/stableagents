import customtkinter as ctk
import tkinter as tk
import webbrowser

class YouTubeBrowserApp(ctk.CTk):
    """
    A modern, professional desktop application to open web pages,
    with a default focus on YouTube. Built with CustomTkinter.
    """
    def __init__(self, *args, **kwargs):
        """
        Initialize the main application window and its components.
        """
        super().__init__(*args, **kwargs)

        # --- Window Configuration ---
        self.title("youtube")
        self.geometry("800x600")
        self.minsize(600, 400)

        # --- Theming ---
        # Set the initial appearance mode based on the system settings.
        ctk.set_appearance_mode("System")
        # Set the default color theme for widgets.
        ctk.set_default_color_theme("blue")

        # --- Responsive Layout Configuration ---
        # Configure the main window's grid layout.
        # The main content frame (row 1) will expand to fill available space.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- UI Component Creation ---
        self._create_top_frame()
        self._create_main_frame()
        self._create_status_bar()

    def _create_top_frame(self):
        """
        Create the top frame containing the URL entry, Go button, and theme switcher.
        """
        self.top_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        self.top_frame.grid(row=0, column=0, sticky="ew", padx=10, pady=(10, 5))

        # Configure the top frame's grid layout to be responsive.
        # The URL entry (column 1) will expand.
        self.top_frame.grid_columnconfigure(1, weight=1)

        # URL Label
        self.url_label = ctk.CTkLabel(self.top_frame, text="URL:")
        self.url_label.grid(row=0, column=0, padx=(0, 5), pady=5)

        # URL Entry
        self.url_entry_var = tk.StringVar(value="https://www.youtube.com")
        self.url_entry = ctk.CTkEntry(self.top_frame, textvariable=self.url_entry_var)
        self.url_entry.grid(row=0, column=1, sticky="ew", padx=5, pady=5)
        # Bind the <Return> key to the go button's action
        self.url_entry.bind("<Return>", self._on_go_button_click)

        # Go Button
        self.go_button = ctk.CTkButton(self.top_frame, text="Go", width=50, command=self._on_go_button_click)
        self.go_button.grid(row=0, column=2, padx=5, pady=5)

        # Theme Switcher OptionMenu
        self.theme_menu = ctk.CTkOptionMenu(
            self.top_frame,
            values=["Light", "Dark", "System"],
            command=self._change_appearance_mode
        )
        self.theme_menu.grid(row=0, column=3, padx=(5, 0), pady=5)

    def _create_main_frame(self):
        """
        Create the main content area with placeholder text.
        """
        self.main_frame = ctk.CTkFrame(self)
        self.main_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=(5, 10))

        # Configure grid to center the label inside
        self.main_frame.grid_rowconfigure(0, weight=1)
        self.main_frame.grid_columnconfigure(0, weight=1)

        # Instructional Label
        info_text = (
            "Welcome to the YouTube Browser!\n\n"
            "Enter a web address in the URL bar above and press 'Go' or hit Enter.\n"
            "The page will open in your computer's default web browser."
        )
        self.info_label = ctk.CTkLabel(
            self.main_frame,
            text=info_text,
            font=ctk.CTkFont(size=14),
            justify="center",
            wraplength=400
        )
        self.info_label.grid(row=0, column=0, padx=20, pady=20)

    def _create_status_bar(self):
        """
        Create a simple status bar at the bottom for user feedback.
        """
        self.status_bar = ctk.CTkLabel(self, text="Ready", anchor="w", font=ctk.CTkFont(size=12))
        self.status_bar.grid(row=2, column=0, sticky="ew", padx=10, pady=(0, 5))

    # --- Event Handlers and Functionality ---

    def _on_go_button_click(self, event=None):
        """
        Handles the event when the 'Go' button is clicked or Enter is pressed.
        Opens the specified URL in the default web browser.
        """
        url = self.url_entry_var.get().strip()
        if not url:
            self._update_status("Error: URL cannot be empty.", "error")
            return

        # A simple check to ensure the URL is somewhat valid
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        try:
            # Open URL in a new tab of the default browser (new=2)
            webbrowser.open(url, new=2)
            self._update_status(f"Successfully opened: {url}", "success")
        except Exception as e:
            # Handle potential errors from the webbrowser module
            self._update_status(f"Error: Could not open URL. {e}", "error")

    def _change_appearance_mode(self, new_mode: str):
        """
        Changes the application's appearance mode (Light/Dark/System).
        """
        ctk.set_appearance_mode(new_mode)
        self._update_status(f"Theme changed to {new_mode}.", "info")

    def _update_status(self, message: str, level: str = "info"):
        """
        Updates the status bar with a message and appropriate color.
        Levels: 'info', 'success', 'error'.
        """
        self.status_bar.configure(text=message)
        
        # Change text color based on message level for better feedback
        if level == "success":
            self.status_bar.configure(text_color=("green", "lightgreen"))
        elif level == "error":
            self.status_bar.configure(text_color=("red", "salmon"))
        else: # 'info' or default
            # Use the default theme's text color
            self.status_bar.configure(text_color=ctk.ThemeManager.theme["CTkLabel"]["text_color"])

        # Reset color after a few seconds
        self.after(4000, lambda: self._update_status("Ready", "info"))


def main():
    """
    Main function to initialize and run the application.
    """
    app = YouTubeBrowserApp()
    app.mainloop()

if __name__ == "__main__":
    # This is the proper entry point for the application.
    main()