# =============================================================================
# Browser - A Modern YouTube Browser
#
# A simple, modern desktop web browser built with CustomTkinter,
# designed to provide a clean interface for browsing YouTube.
#
# Requirements for running this script:
# 1. Python 3.x
# 2. CustomTkinter: pip install customtkinter
# 3. tkinterweb:   pip install tkinterweb
# =============================================================================

import customtkinter as ctk
import tkinter as tk
from tkinter import messagebox
try:
    from tkinterweb import HtmlFrame
except ImportError:
    messagebox.showerror(
        "Module Not Found",
        "The 'tkinterweb' library is required. Please install it using: pip install tkinterweb"
    )
    exit()

# --- Main Application Class ---
class App(ctk.CTk):
    """
    Main application class for the Browser.
    This class initializes the application window and all its components.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Window Setup ---
        self.title("Browser")
        self.geometry("1280x720")  # Set a default window size
        self.minsize(800, 600)     # Set a minimum window size

        # --- Theming ---
        # Set initial theme based on system settings
        ctk.set_appearance_mode("System")

        # --- Main Layout Configuration ---
        # Configure the main grid to be responsive.
        # The grid has 1 row and 2 columns (sidebar and main content).
        self.grid_rowconfigure(0, weight=1)
        self.grid_columnconfigure(1, weight=1)

        # --- Create UI Components ---
        self._create_sidebar()
        self._create_main_content()

        # --- Window Management ---
        # Handle the window closing event gracefully
        self.protocol("WM_DELETE_WINDOW", self._on_closing)

    def _create_sidebar(self):
        """Creates the sidebar frame with settings and controls."""
        # The sidebar frame holds application-level settings.
        self.sidebar_frame = ctk.CTkFrame(self, width=200, corner_radius=0)
        self.sidebar_frame.grid(row=0, column=0, sticky="nsw")
        self.sidebar_frame.grid_rowconfigure(4, weight=1) # Pushes widgets to the top

        # App Logo/Title
        self.logo_label = ctk.CTkLabel(self.sidebar_frame, text="Browser", font=ctk.CTkFont(size=20, weight="bold"))
        self.logo_label.grid(row=0, column=0, padx=20, pady=(20, 10))

        # Appearance Mode Control
        self.appearance_mode_label = ctk.CTkLabel(self.sidebar_frame, text="Appearance Mode:", anchor="w")
        self.appearance_mode_label.grid(row=5, column=0, padx=20, pady=(10, 0))
        self.appearance_mode_optionemenu = ctk.CTkOptionMenu(self.sidebar_frame, values=["Light", "Dark", "System"],
                                                               command=self._change_appearance_mode_event)
        self.appearance_mode_optionemenu.grid(row=6, column=0, padx=20, pady=(10, 10))
        self.appearance_mode_optionemenu.set("System") # Set default value

    def _create_main_content(self):
        """Creates the main content area, including browser controls and the web view."""
        # This frame will hold the address bar, navigation buttons, and the web viewer.
        self.main_frame = ctk.CTkFrame(self, corner_radius=0)
        self.main_frame.grid(row=0, column=1, sticky="nsew")
        self.main_frame.grid_rowconfigure(1, weight=1)    # Web view row should expand
        self.main_frame.grid_columnconfigure(0, weight=1) # Main content column should expand

        # --- Navigation Controls Frame ---
        self.nav_frame = ctk.CTkFrame(self.main_frame, corner_radius=0)
        self.nav_frame.grid(row=0, column=0, sticky="new", padx=10, pady=10)
        self.nav_frame.grid_columnconfigure(3, weight=1) # URL entry should expand

        # Back Button
        self.back_button = ctk.CTkButton(self.nav_frame, text="<", width=30, command=self._go_back)
        self.back_button.grid(row=0, column=0, padx=(0, 5))

        # Forward Button
        self.forward_button = ctk.CTkButton(self.nav_frame, text=">", width=30, command=self._go_forward)
        self.forward_button.grid(row=0, column=1, padx=5)

        # Reload Button
        self.reload_button = ctk.CTkButton(self.nav_frame, text="↻", width=30, command=self._reload_page)
        self.reload_button.grid(row=0, column=2, padx=5)

        # URL Entry Bar
        self.url_entry = ctk.CTkEntry(self.nav_frame, placeholder_text="Enter URL and press Enter")
        self.url_entry.grid(row=0, column=3, sticky="ew", padx=5)
        self.url_entry.bind("<Return>", self._navigate_to_url) # Bind Enter key to navigate

        # Go Button
        self.go_button = ctk.CTkButton(self.nav_frame, text="Go", width=50, command=self._navigate_to_url)
        self.go_button.grid(row=0, column=4, padx=(5, 0))

        # --- Web View Frame ---
        # The HtmlFrame from tkinterweb is used to render the web content.
        self.webview = HtmlFrame(self.main_frame, messages_enabled=False) # Disable JS alerts
        self.webview.grid(row=1, column=0, sticky="nsew", padx=10, pady=(0, 10))

        # --- Initial Page Load ---
        self.initial_url = "https://www.youtube.com"
        self.url_entry.insert(0, self.initial_url)
        self.webview.load_url(self.initial_url)

        # --- Event Binding for Web View ---
        # Update the URL bar when the user navigates within the page.
        self.webview.on_url_change = self._update_url_bar

    # --- Event Handlers and Functionality ---

    def _navigate_to_url(self, event=None):
        """
        Navigates the web view to the URL entered in the URL bar.
        Handles basic URL validation.
        """
        url = self.url_entry.get().strip()
        if not url:
            messagebox.showwarning("Empty URL", "Please enter a URL to navigate.")
            return

        # Basic check to add http/https if missing for convenience
        if not (url.startswith("http://") or url.startswith("https://")):
            url = "https://" + url

        try:
            self.webview.load_url(url)
        except Exception as e:
            # Provide user-friendly error feedback
            messagebox.showerror("Navigation Error", f"Could not load the URL: {url}\n\nError: {e}")

    def _go_back(self):
        """Navigates to the previous page in history."""
        try:
            self.webview.history_back()
        except IndexError:
            # This can happen if there's no history to go back to.
            # We can silently ignore it or provide feedback.
            pass

    def _go_forward(self):
        """Navigates to the next page in history."""
        try:
            self.webview.history_forward()
        except IndexError:
            # This can happen if there's no forward history.
            pass

    def _reload_page(self):
        """Reloads the current page."""
        self.webview.reload()

    def _update_url_bar(self, url):
        """Callback function to update the URL bar when navigation occurs."""
        self.url_entry.delete(0, tk.END)
        self.url_entry.insert(0, url)

    def _change_appearance_mode_event(self, new_appearance_mode: str):
        """Changes the application's theme (Light, Dark, System)."""
        ctk.set_appearance_mode(new_appearance_mode)

    def _on_closing(self):
        """Handles the window closing event."""
        # You can add prompts here like "Are you sure you want to quit?"
        self.destroy()

# --- Main Function and Entry Point ---

def main():
    """Main function to initialize and run the application."""
    app = App()
    app.mainloop()

if __name__ == "__main__":
    main()