import customtkinter as ctk
import tkinter as tk
import math

class ScientificCalculatorApp(ctk.CTk):
    """
    A modern scientific calculator desktop application built with CustomTkinter.
    It supports basic arithmetic, scientific functions, and light/dark modes.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # --- Window Setup ---
        self.title("Scientific Calculator")
        self.geometry("400x600")
        self.minsize(380, 580)

        # --- State Variables ---
        # StringVar to hold the expression in the display
        self.expression_var = tk.StringVar()
        # Flag to check if the last operation was a calculation
        self.is_result_displayed = False

        # --- Main Layout Configuration ---
        # The main window is configured into 2 rows.
        # The display (row 0) will not expand vertically.
        # The button frame (row 1) will take up all available vertical space.
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)

        # --- Create and Place Widgets ---
        self._create_widgets()

    def _create_widgets(self):
        """Creates and places all the UI components in the window."""
        # --- Display Screen ---
        # A CTkEntry is used for the display, but configured to be read-only.
        # A large font is used for better readability.
        display_font = ctk.CTkFont(family="Arial", size=40, weight="bold")
        display = ctk.CTkEntry(self,
                               textvariable=self.expression_var,
                               font=display_font,
                               justify="right",
                               border_width=2,
                               corner_radius=10,
                               state="readonly")
        display.grid(row=0, column=0, columnspan=2, padx=10, pady=15, sticky="nsew")

        # --- Buttons Frame ---
        # A CTkFrame holds all the calculator buttons.
        buttons_frame = ctk.CTkFrame(self, corner_radius=10)
        buttons_frame.grid(row=1, column=0, padx=10, pady=10, sticky="nsew")

        # Configure the button frame's grid to be responsive. 5 columns, 6 rows.
        for i in range(6):
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):
            buttons_frame.grid_columnconfigure(i, weight=1)

        # --- Button Definitions ---
        # A list of tuples defining the text, grid position, and type of each button.
        # Button types: 'num' (numbers/operators), 'op' (special operators), 'eq' (equals)
        buttons = [
            # Row 0
            ('sin', 0, 0, 'op'), ('cos', 0, 1, 'op'), ('tan', 0, 2, 'op'), ('log', 0, 3, 'op'), ('ln', 0, 4, 'op'),
            # Row 1
            ('(', 1, 0, 'op'), (')', 1, 1, 'op'), ('√', 1, 2, 'op'), ('x²', 1, 3, 'op'), ('^', 1, 4, 'op'),
            # Row 2
            ('7', 2, 0, 'num'), ('8', 2, 1, 'num'), ('9', 2, 2, 'num'), ('⌫', 2, 3, 'op'), ('C', 2, 4, 'op'),
            # Row 3
            ('4', 3, 0, 'num'), ('5', 3, 1, 'num'), ('6', 3, 2, 'num'), ('*', 3, 3, 'num'), ('/', 3, 4, 'num'),
            # Row 4
            ('1', 4, 0, 'num'), ('2', 4, 1, 'num'), ('3', 4, 2, 'num'), ('+', 4, 3, 'num'), ('-', 4, 4, 'num'),
            # Row 5
            ('0', 5, 0, 'num'), ('.', 5, 1, 'num'), ('π', 5, 2, 'op'), ('%', 5, 3, 'op'), ('=', 5, 4, 'eq')
        ]

        # --- Create and Place Buttons ---
        button_font = ctk.CTkFont(family="Arial", size=20, weight="bold")
        for (text, row, col, btn_type) in buttons:
            # Assign command based on the button text
            if text == 'C':
                command = self._clear_all
            elif text == '⌫':
                command = self._backspace
            elif text == '=':
                command = self._calculate_result
            else:
                # Use a lambda to pass the button text to the handler
                command = lambda t=text: self._on_button_press(t)

            # Define colors based on button type
            fg_color = "#343638"
            hover_color = "#4E5053"
            if btn_type == 'num':
                fg_color = "#5F6368"
                hover_color = "#7F8388"
            elif btn_type == 'eq':
                fg_color = "#4285F4"
                hover_color = "#62A5F4"

            button = ctk.CTkButton(buttons_frame,
                                   text=text,
                                   font=button_font,
                                   command=command,
                                   fg_color=fg_color,
                                   hover_color=hover_color,
                                   corner_radius=8)
            button.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")

        # --- Theme Switcher ---
        # A small frame at the bottom for controls like the theme switch.
        control_frame = ctk.CTkFrame(self, height=50, corner_radius=0)
        control_frame.grid(row=2, column=0, columnspan=2, sticky="sew")
        control_frame.grid_columnconfigure((0, 2), weight=1) # Center the switch

        theme_switch = ctk.CTkSwitch(control_frame,
                                     text="Light/Dark Mode",
                                     command=self._toggle_theme,
                                     onvalue="dark", offvalue="light")
        theme_switch.grid(row=0, column=1, padx=10, pady=10)
        theme_switch.select() # Start in dark mode by default

    # --- Event Handlers ---
    def _on_button_press(self, char):
        """
        Handles presses for numbers and standard operators.
        Appends the character to the expression.
        """
        # If a result is currently displayed, clear the display before adding new input
        if self.is_result_displayed:
            # Allow operators to continue calculation with the result
            if char in ['+', '-', '*', '/', '^', '%']:
                current_expression = self.expression_var.get()
                self.expression_var.set(current_expression + char)
            else: # Clear for new number
                self.expression_var.set(char)
            self.is_result_displayed = False
        else:
            # Special handling for scientific functions to add the opening parenthesis
            if char in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
                self.expression_var.set(self.expression_var.get() + f"{char}(")
            elif char == 'x²':
                self.expression_var.set(self.expression_var.get() + "**2")
            elif char == '^':
                self.expression_var.set(self.expression_var.get() + "**")
            elif char == 'π':
                 self.expression_var.set(self.expression_var.get() + "pi")
            elif char == '%':
                self.expression_var.set(self.expression_var.get() + "*0.01")
            else:
                self.expression_var.set(self.expression_var.get() + char)

    def _calculate_result(self):
        """
        Evaluates the expression in the display.
        Handles errors by displaying 'Error'.
        """
        try:
            expression = self.expression_var.get()
            # Replace user-friendly names with their math module equivalents for eval()
            # This is safer than direct eval as it limits function calls.
            safe_expression = expression.replace('sin', 'math.sin')
            safe_expression = safe_expression.replace('cos', 'math.cos')
            safe_expression = safe_expression.replace('tan', 'math.tan')
            safe_expression = safe_expression.replace('log', 'math.log10') # log is base 10
            safe_expression = safe_expression.replace('ln', 'math.log')    # ln is natural log
            safe_expression = safe_expression.replace('√', 'math.sqrt')
            safe_expression = safe_expression.replace('pi', 'math.pi')

            # Evaluate the expression
            result = eval(safe_expression)
            
            # Format result to avoid unnecessary decimals (e.g., 5.0 -> 5)
            if result == int(result):
                result = int(result)
                
            self.expression_var.set(str(result))
            self.is_result_displayed = True
        except (SyntaxError, ZeroDivisionError, TypeError, NameError, ValueError) as e:
            self.expression_var.set("Error")
            print(f"Calculation Error: {e}") # Log the error for debugging
            self.is_result_displayed = True
        except Exception as e:
            self.expression_var.set("Error")
            print(f"An unexpected error occurred: {e}")
            self.is_result_displayed = True


    def _clear_all(self):
        """Clears the entire display."""
        self.expression_var.set("")
        self.is_result_displayed = False

    def _backspace(self):
        """Removes the last character from the display."""
        if self.is_result_displayed:
            self._clear_all()
        else:
            current_expression = self.expression_var.get()
            self.expression_var.set(current_expression[:-1])

    def _toggle_theme(self):
        """Toggles the application's appearance between 'light' and 'dark' modes."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)

def main():
    """Main function to initialize and run the application."""
    # Set the initial appearance mode and color theme for the application
    ctk.set_appearance_mode("dark")  # Can be "System", "Dark", "Light"
    ctk.set_default_color_theme("blue")  # Themes: "blue", "green", "dark-blue"

    # Create the application instance and run the main loop
    app = ScientificCalculatorApp()
    app.mainloop()

if __name__ == "__main__":
    main()