import customtkinter as ctk
import tkinter as tk

# Set the default appearance mode and color theme for the application
ctk.set_appearance_mode("System")  # Options: "System" (default), "Dark", "Light"
ctk.set_default_color_theme("blue")  # Options: "blue" (default), "green", "dark-blue"

class SimpleCalculator(ctk.CTk):
    """
    A modern, responsive calculator application built with CustomTkinter.

    This class encapsulates the entire application, including the UI,
    event handling, and calculation logic.
    """
    def __init__(self):
        super().__init__()

        # --- Window Setup ---
        self.title("SimpleCalculator")
        self.geometry("380x550")
        self.minsize(320, 500)

        # --- State Variables ---
        self.current_expression = ""  # The string for the main display (bottom)
        self.total_expression = ""    # The string for the history display (top)

        # --- Main Layout Configuration ---
        # The main window is configured into 2 rows and 1 column.
        # The display frame will be in row 0, and the button frame in row 1.
        self.grid_rowconfigure(0, weight=2)    # Display gets 2/7 of the vertical space
        self.grid_rowconfigure(1, weight=5)    # Buttons get 5/7 of the vertical space
        self.grid_columnconfigure(0, weight=1) # The single column expands to fill width

        # --- UI Initialization ---
        self._setup_ui()

    def _setup_ui(self):
        """Initializes and packs all UI components."""
        self._create_display_frame()
        self._create_buttons_frame()

    def _create_display_frame(self):
        """Creates the frame that holds the display labels."""
        display_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        display_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

        # Configure the grid inside the display frame
        display_frame.grid_rowconfigure(0, weight=1)
        display_frame.grid_rowconfigure(1, weight=1)
        display_frame.grid_rowconfigure(2, weight=2)
        display_frame.grid_columnconfigure(0, weight=1)

        # --- Theme Toggle ---
        theme_frame = ctk.CTkFrame(display_frame, fg_color="transparent")
        theme_frame.grid(row=0, column=0, sticky="ne", padx=5, pady=5)
        
        theme_label = ctk.CTkLabel(theme_frame, text="Theme:")
        theme_label.pack(side="left", padx=(0, 5))

        self.theme_menu = ctk.CTkOptionMenu(
            theme_frame,
            values=["System", "Light", "Dark"],
            command=self._change_theme,
            width=90
        )
        self.theme_menu.set("System")
        self.theme_menu.pack(side="left")

        # --- Display Labels ---
        # Label for showing the full expression history (e.g., "78+")
        self.total_expression_label = ctk.CTkLabel(
            display_frame,
            text="",
            font=ctk.CTkFont(size=20),
            text_color=("gray30", "gray70"),
            anchor="e"
        )
        self.total_expression_label.grid(row=1, column=0, sticky="sew", padx=10)

        # Main label for current input and results
        self.current_expression_label = ctk.CTkLabel(
            display_frame,
            text="0",
            font=ctk.CTkFont(size=48, weight="bold"),
            anchor="e"
        )
        self.current_expression_label.grid(row=2, column=0, sticky="sew", padx=10)

    def _create_buttons_frame(self):
        """Creates the frame that holds all the calculator buttons."""
        buttons_frame = ctk.CTkFrame(self, corner_radius=0, fg_color="transparent")
        buttons_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

        # --- Button Layout Definition ---
        # A list of lists representing the grid of buttons.
        # The 'span' key indicates that a button should span multiple columns.
        button_layout = [
            {'text': 'C', 'type': 'special', 'row': 0, 'col': 0},
            {'text': '⌫', 'type': 'special', 'row': 0, 'col': 1},
            {'text': '%', 'type': 'operator', 'row': 0, 'col': 2},
            {'text': '÷', 'type': 'operator', 'row': 0, 'col': 3},
            
            {'text': '7', 'type': 'number', 'row': 1, 'col': 0},
            {'text': '8', 'type': 'number', 'row': 1, 'col': 1},
            {'text': '9', 'type': 'number', 'row': 1, 'col': 2},
            {'text': '×', 'type': 'operator', 'row': 1, 'col': 3},

            {'text': '4', 'type': 'number', 'row': 2, 'col': 0},
            {'text': '5', 'type': 'number', 'row': 2, 'col': 1},
            {'text': '6', 'type': 'number', 'row': 2, 'col': 2},
            {'text': '-', 'type': 'operator', 'row': 2, 'col': 3},

            {'text': '1', 'type': 'number', 'row': 3, 'col': 0},
            {'text': '2', 'type': 'number', 'row': 3, 'col': 1},
            {'text': '3', 'type': 'number', 'row': 3, 'col': 2},
            {'text': '+', 'type': 'operator', 'row': 3, 'col': 3},

            {'text': '0', 'type': 'number', 'row': 4, 'col': 0, 'span': 2},
            {'text': '.', 'type': 'number', 'row': 4, 'col': 2},
            {'text': '=', 'type': 'equals', 'row': 4, 'col': 3},
        ]
        
        # Configure grid columns and rows to be responsive
        for i in range(5): # 5 rows
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(4): # 4 columns
            buttons_frame.grid_columnconfigure(i, weight=1)
            
        # --- Create and Place Buttons ---
        for button_info in button_layout:
            self._create_button(buttons_frame, button_info)

    def _create_button(self, parent, info):
        """Helper method to create a single styled button."""
        text = info['text']
        btn_type = info['type']
        row = info['row']
        col = info['col']
        span = info.get('span', 1)

        # --- Button Styling ---
        # Define styles based on button type for better UX
        style = {
            'font': ctk.CTkFont(size=24),
            'corner_radius': 8,
            'command': lambda t=text: self._on_button_press(t)
        }

        if btn_type == 'number':
            style['fg_color'] = ("#F2F2F2", "#3C3C3C")
            style['hover_color'] = ("#E8E8E8", "#505050")
            style['text_color'] = ("#000000", "#FFFFFF")
        elif btn_type == 'operator':
            style['fg_color'] = ("#FFA500", "#FF9500") # Orange
            style['hover_color'] = ("#FFB733", "#FFA726")
            style['text_color'] = ("#FFFFFF", "#FFFFFF")
        elif btn_type == 'special':
            style['fg_color'] = ("#D3D3D3", "#A5A5A5") # Light Gray
            style['hover_color'] = ("#C0C0C0", "#BDBDBD")
            style['text_color'] = ("#000000", "#000000")
        elif btn_type == 'equals':
            style['fg_color'] = ("#FFA500", "#FF9500") # Orange
            style['hover_color'] = ("#FFB733", "#FFA726")
            style['text_color'] = ("#FFFFFF", "#FFFFFF")

        button = ctk.CTkButton(parent, text=text, **style)
        button.grid(row=row, column=col, columnspan=span, sticky="nsew", padx=5, pady=5)

    def _on_button_press(self, symbol):
        """Handles all button press events and directs logic."""
        if symbol.isdigit() or symbol == '.':
            self._handle_digit(symbol)
        elif symbol in ['+', '-', '×', '÷', '%']:
            self._handle_operator(symbol)
        elif symbol == 'C':
            self._clear_all()
        elif symbol == '⌫':
            self._backspace()
        elif symbol == '=':
            self._calculate_result()
        
        self._update_display()

    def _handle_digit(self, digit):
        """Handles number and decimal point inputs."""
        if self.current_expression == "0" and digit != '.':
            self.current_expression = digit
        elif digit == '.' and '.' in self.current_expression:
            return  # Prevent multiple decimal points
        else:
            self.current_expression += digit

    def _handle_operator(self, op):
        """Handles operator inputs."""
        if self.current_expression:
            self.total_expression += self.current_expression + " " + op + " "
            self.current_expression = ""

    def _clear_all(self):
        """Clears all expressions and resets the display."""
        self.current_expression = "0"
        self.total_expression = ""

    def _backspace(self):
        """Removes the last character from the current expression."""
        if len(self.current_expression) > 1:
            self.current_expression = self.current_expression[:-1]
        else:
            self.current_expression = "0"

    def _calculate_result(self):
        """Evaluates the final expression."""
        if not self.total_expression or not self.current_expression:
            return

        full_expression_str = self.total_expression + self.current_expression
        
        # Replace display symbols with Python operators for evaluation
        eval_str = full_expression_str.replace('×', '*').replace('÷', '/').replace('%', '/100*')
        
        try:
            # --- Perform Calculation ---
            result = eval(eval_str)

            # Format result nicely (remove unnecessary .0)
            if result == int(result):
                result = int(result)

            self.current_expression = str(result)
            self.total_expression = ""
            
        except ZeroDivisionError:
            self.current_expression = "Error"
            self.total_expression = ""
        except (SyntaxError, NameError, ValueError):
            self.current_expression = "Invalid"
            self.total_expression = ""
            
    def _update_display(self):
        """Updates the text on the display labels."""
        self.current_expression_label.configure(text=self.current_expression or "0")
        self.total_expression_label.configure(text=self.total_expression)

    def _change_theme(self, new_theme: str):
        """Changes the application's appearance mode."""
        ctk.set_appearance_mode(new_theme)


def main():
    """The main entry point for the application."""
    app = SimpleCalculator()
    app.mainloop()


if __name__ == "__main__":
    main()