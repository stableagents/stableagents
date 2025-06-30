import customtkinter as ctk
import tkinter as tk
import os
import sys
import base64

# --- Main Application Class ---
class CalculatorApp(ctk.CTk):
    """
    A modern calculator application built with CustomTkinter.
    It features a responsive UI, dark/light mode, color themes, and error handling.
    """

    def __init__(self, **kwargs):
        """
        Initialize the main application window.
        """
        super().__init__(**kwargs)

        # --- Window Configuration ---
        self.title("Modern Calculator")
        self.geometry("400x600")  # Set an initial size
        self.minsize(350, 550)    # Set a minimum size to maintain usability

        # Set a modern icon (embedded as base64 to keep the script self-contained)
        self._set_icon()

        # --- State Variables ---
        self.expression_str_var = tk.StringVar(value="")
        self.error_state = False

        # --- Theming Setup ---
        ctk.set_appearance_mode("System")  # Options: "System", "Dark", "Light"
        ctk.set_default_color_theme("blue") # Options: "blue", "green", "dark-blue"

        # --- UI Initialization ---
        self._create_widgets()
        self._configure_grid()

    def _set_icon(self):
        """
        Sets the application icon. The icon is encoded in base64 to avoid
        depending on an external file, making the script portable.
        """
        # A simple calculator icon encoded in base64
        icon_data = base64.b64decode("""
            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
        """)
        try:
            icon_image = tk.PhotoImage(data=icon_data)
            self.iconphoto(True, icon_image)
        except tk.TclError:
            # This can happen on some systems if photoimage fails.
            # The app will run without an icon.
            print("Warning: Could not set application icon.")

    def _configure_grid(self):
        """
        Configures the grid layout to be responsive.
        Rows and columns will expand/contract with the window size.
        """
        self.grid_columnconfigure((0, 1, 2, 3), weight=1)
        self.grid_rowconfigure(0, weight=1) # Settings row
        self.grid_rowconfigure(1, weight=2) # Display row
        self.grid_rowconfigure((2, 3, 4, 5, 6), weight=2) # Button rows

    def _create_widgets(self):
        """
        Creates and places all the UI widgets in the window.
        """
        # --- Settings Frame ---
        settings_frame = ctk.CTkFrame(self, fg_color="transparent")
        settings_frame.grid(row=0, column=0, columnspan=4, padx=10, pady=5, sticky="ew")
        settings_frame.grid_columnconfigure((1, 3), weight=1)

        # Appearance Mode
        ctk.CTkLabel(settings_frame, text="Theme:").grid(row=0, column=0, padx=(10,5), pady=5)
        self.appearance_menu = ctk.CTkOptionMenu(settings_frame,
                                                 values=["Light", "Dark", "System"],
                                                 command=self._change_appearance_mode)
        self.appearance_menu.grid(row=0, column=1, padx=5, pady=5, sticky="ew")

        # Color Theme
        ctk.CTkLabel(settings_frame, text="Color:").grid(row=0, column=2, padx=(10,5), pady=5)
        self.color_menu = ctk.CTkOptionMenu(settings_frame,
                                             values=["Blue", "Green", "Dark-Blue"],
                                             command=self._change_color_theme)
        self.color_menu.set("Blue")
        self.color_menu.grid(row=0, column=3, padx=5, pady=5, sticky="ew")

        # --- Display Label ---
        display_label = ctk.CTkLabel(self,
                                     textvariable=self.expression_str_var,
                                     font=ctk.CTkFont(size=50, weight="bold"),
                                     anchor="e",
                                     padx=20)
        display_label.grid(row=1, column=0, columnspan=4, padx=10, pady=(5, 10), sticky="nsew")

        # --- Button Creation ---
        # Defines the layout and text for each button
        button_layout = [
            {'text': 'C', 'row': 2, 'col': 0, 'type': 'op'},
            {'text': '<-', 'row': 2, 'col': 1, 'type': 'op'},
            {'text': '%', 'row': 2, 'col': 2, 'type': 'op'},
            {'text': '/', 'row': 2, 'col': 3, 'type': 'op'},
            {'text': '7', 'row': 3, 'col': 0, 'type': 'num'},
            {'text': '8', 'row': 3, 'col': 1, 'type': 'num'},
            {'text': '9', 'row': 3, 'col': 2, 'type': 'num'},
            {'text': '*', 'row': 3, 'col': 3, 'type': 'op'},
            {'text': '4', 'row': 4, 'col': 0, 'type': 'num'},
            {'text': '5', 'row': 4, 'col': 1, 'type': 'num'},
            {'text': '6', 'row': 4, 'col': 2, 'type': 'num'},
            {'text': '-', 'row': 4, 'col': 3, 'type': 'op'},
            {'text': '1', 'row': 5, 'col': 0, 'type': 'num'},
            {'text': '2', 'row': 5, 'col': 1, 'type': 'num'},
            {'text': '3', 'row': 5, 'col': 2, 'type': 'num'},
            {'text': '+', 'row': 5, 'col': 3, 'type': 'op'},
            {'text': '0', 'row': 6, 'col': 0, 'col_span': 2, 'type': 'num'},
            {'text': '.', 'row': 6, 'col': 2, 'type': 'num'},
            {'text': '=', 'row': 6, 'col': 3, 'type': 'eq'}
        ]

        # Define colors for different button types
        num_fg_color = ("#F2F2F2", "#3D3D3D")  # (light_mode, dark_mode)
        num_hover_color = ("#E5E5E5", "#505050")
        op_fg_color = ("#D9D9D9", "#2E2E2E")
        op_hover_color = ("#CCCCCC", "#404040")

        # Loop through the layout to create and place buttons
        for btn_info in button_layout:
            btn = ctk.CTkButton(
                self,
                text=btn_info['text'],
                font=ctk.CTkFont(size=24, weight="bold"),
                command=lambda symbol=btn_info['text']: self._on_button_press(symbol)
            )

            # Apply specific styling based on button type
            if btn_info['type'] == 'num':
                btn.configure(fg_color=num_fg_color, hover_color=num_hover_color)
            elif btn_info['type'] == 'op':
                btn.configure(fg_color=op_fg_color, hover_color=op_hover_color)
            # The 'eq' button will use the default theme color

            # Place button in grid, handling column spans if necessary
            col_span = btn_info.get('col_span', 1)
            btn.grid(row=btn_info['row'], column=btn_info['col'],
                     columnspan=col_span, padx=5, pady=5, sticky="nsew")

    # --- Event Handlers and Functionality ---
    def _on_button_press(self, symbol):
        """
        Handles all button press events.
        """
        current_expression = self.expression_str_var.get()

        # If the calculator is in an error state, any button press (except clear)
        # should clear the display first.
        if self.error_state and symbol != 'C':
            current_expression = ""
            self.error_state = False

        if symbol == 'C':
            # Clear the entire expression
            new_expression = ""
        elif symbol == '<-':
            # Handle backspace
            new_expression = current_expression[:-1]
        elif symbol == '=':
            # Evaluate the expression
            self._evaluate_expression()
            return  # Evaluation handles setting the variable itself
        else:
            # Append the pressed symbol to the expression
            new_expression = current_expression + symbol

        # Update the display
        self.expression_str_var.set(new_expression)

    def _evaluate_expression(self):
        """
        Evaluates the current mathematical expression.
        Includes error handling for invalid syntax or math errors.
        """
        current_expression = self.expression_str_var.get()

        # Sanitize expression for evaluation
        # Replace '%' with '/100*' to function as a percentage
        # A more robust solution might use a proper parser, but this is fine for a basic calculator.
        sanitized_expression = current_expression.replace('%', '/100')

        try:
            # IMPORTANT: eval() can be a security risk if used with untrusted input.
            # In this controlled calculator environment, it's acceptable.
            result = eval(sanitized_expression)

            # If the result is a whole number, display it as an integer
            if result == int(result):
                result = int(result)
            else:
                # Limit floating point numbers to a reasonable number of digits
                result = round(result, 8)

            # Update display with the result
            self.expression_str_var.set(str(result))

        except (SyntaxError, ZeroDivisionError, TypeError, NameError):
            # If any error occurs, display "Error" and set the error state
            self.expression_str_var.set("Error")
            self.error_state = True
        except Exception:
            # Catch any other unexpected errors
            self.expression_str_var.set("Error")
            self.error_state = True

    def _change_appearance_mode(self, new_mode):
        """Callback for the appearance mode OptionMenu."""
        ctk.set_appearance_mode(new_mode)

    def _change_color_theme(self, new_color):
        """
        Callback for the color theme OptionMenu.
        Note: A restart might be needed for all UI elements to fully update color.
        """
        ctk.set_default_color_theme(new_color.lower())
        # A more advanced approach would be to recreate widgets or update them manually.
        # For simplicity, we just change the default and let new widgets use it.

# --- Main function and proper entry point ---
def main():
    """
    Main function to create and run the application.
    """
    app = CalculatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()