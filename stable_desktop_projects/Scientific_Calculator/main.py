import customtkinter as ctk
import tkinter as tk
import math
from PIL import Image, ImageDraw, ImageFont
import io
import base64
import requests
from typing import Dict, Tuple, Optional

class IconGenerator:
    """Generates modern, beautiful icons for calculator buttons."""
    
    def __init__(self):
        self.icon_cache = {}
        self.colors = {
            'primary': '#4285F4',
            'secondary': '#5F6368', 
            'accent': '#34A853',
            'warning': '#EA4335',
            'dark_bg': '#2D2D2D',
            'light_bg': '#FFFFFF',
            'dark_text': '#FFFFFF',
            'light_text': '#000000'
        }
    
    def create_icon(self, text: str, size: int = 32, bg_color: str = None, 
                   text_color: str = None, icon_type: str = 'default') -> Image.Image:
        """Creates a custom icon with the given text and styling."""
        
        # Create a new image with alpha channel for transparency
        img = Image.new('RGBA', (size, size), (0, 0, 0, 0))
        draw = ImageDraw.Draw(img)
        
        # Set colors based on icon type
        if bg_color is None:
            if icon_type == 'function':
                bg_color = self.colors['accent']
            elif icon_type == 'operator':
                bg_color = self.colors['warning']
            elif icon_type == 'equals':
                bg_color = self.colors['primary']
            else:
                bg_color = self.colors['secondary']
        
        if text_color is None:
            text_color = self.colors['dark_text']
        
        # Draw rounded rectangle background
        padding = size // 8
        rect_coords = [padding, padding, size - padding, size - padding]
        draw.rounded_rectangle(rect_coords, radius=size//6, fill=bg_color)
        
        # Calculate font size based on text length
        font_size = max(size // 3, 8)
        if len(text) > 2:
            font_size = max(size // 4, 6)
        
        try:
            # Try to use a modern font
            font = ImageFont.truetype("Arial", font_size)
        except:
            font = ImageFont.load_default()
        
        # Center the text
        bbox = draw.textbbox((0, 0), text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (size - text_width) // 2
        y = (size - text_height) // 2
        
        # Draw the text
        draw.text((x, y), text, fill=text_color, font=font)
        
        return img
    
    def get_icon(self, text: str, icon_type: str = 'default') -> Image.Image:
        """Gets an icon from cache or creates a new one."""
        cache_key = f"{text}_{icon_type}"
        if cache_key not in self.icon_cache:
            self.icon_cache[cache_key] = self.create_icon(text, icon_type=icon_type)
        return self.icon_cache[cache_key]

class ModernScientificCalculator(ctk.CTk):
    """
    A modern scientific calculator with beautiful icons and enhanced UI.
    Built with CustomTkinter and custom icon generation.
    """
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Initialize icon generator
        self.icon_generator = IconGenerator()
        
        # --- Window Setup ---
        self.title("Modern Scientific Calculator")
        self.geometry("450x700")
        self.minsize(420, 650)
        
        # Set app icon
        self._set_app_icon()
        
        # --- State Variables ---
        self.expression_var = tk.StringVar()
        self.is_result_displayed = False
        self.history = []
        
        # --- Main Layout Configuration ---
        self.grid_rowconfigure(1, weight=1)
        self.grid_columnconfigure(0, weight=1)
        
        # --- Create and Place Widgets ---
        self._create_widgets()
        
        # Set initial theme
        ctk.set_appearance_mode("dark")
        ctk.set_default_color_theme("blue")
    
    def _set_app_icon(self):
        """Sets a custom app icon."""
        try:
            # Create a calculator icon
            icon = self.icon_generator.create_icon("🧮", size=64, 
                                                 bg_color=self.icon_generator.colors['primary'],
                                                 icon_type='equals')
            
            # Convert to PhotoImage
            icon_tk = self._pil_to_photoimage(icon)
            self.iconphoto(True, icon_tk)
        except Exception as e:
            print(f"Could not set app icon: {e}")
    
    def _pil_to_photoimage(self, pil_image: Image.Image) -> tk.PhotoImage:
        """Converts PIL Image to tkinter PhotoImage."""
        # Convert to RGB if necessary
        if pil_image.mode != 'RGB':
            pil_image = pil_image.convert('RGB')
        
        # Convert to bytes
        buffer = io.BytesIO()
        pil_image.save(buffer, format='PNG')
        buffer.seek(0)
        
        # Create PhotoImage
        return tk.PhotoImage(data=buffer.getvalue())
    
    def _create_widgets(self):
        """Creates and places all the UI components."""
        
        # --- Header with Title and Theme Toggle ---
        header_frame = ctk.CTkFrame(self, height=60, corner_radius=0)
        header_frame.grid(row=0, column=0, columnspan=2, sticky="ew", padx=0, pady=0)
        header_frame.grid_columnconfigure(1, weight=1)
        
        # App title with icon
        title_label = ctk.CTkLabel(header_frame, 
                                  text="🧮 Modern Calculator", 
                                  font=ctk.CTkFont(size=18, weight="bold"))
        title_label.grid(row=0, column=0, padx=15, pady=15, sticky="w")
        
        # Theme toggle
        theme_switch = ctk.CTkSwitch(header_frame,
                                   text="🌙",
                                   command=self._toggle_theme,
                                   onvalue="dark", offvalue="light",
                                   width=60)
        theme_switch.grid(row=0, column=2, padx=15, pady=15, sticky="e")
        theme_switch.select()  # Start in dark mode
        
        # --- Display Screen ---
        display_frame = ctk.CTkFrame(self, corner_radius=15)
        display_frame.grid(row=1, column=0, columnspan=2, padx=15, pady=10, sticky="ew")
        display_frame.grid_columnconfigure(0, weight=1)
        
        # Expression display
        display_font = ctk.CTkFont(family="Arial", size=32, weight="bold")
        self.display = ctk.CTkEntry(display_frame,
                                   textvariable=self.expression_var,
                                   font=display_font,
                                   justify="right",
                                   border_width=0,
                                   corner_radius=10,
                                   state="readonly",
                                   height=60)
        self.display.grid(row=0, column=0, padx=10, pady=10, sticky="ew")
        
        # --- Buttons Frame ---
        buttons_frame = ctk.CTkFrame(self, corner_radius=15)
        buttons_frame.grid(row=2, column=0, padx=15, pady=10, sticky="nsew")
        
        # Configure grid
        for i in range(7):  # 7 rows
            buttons_frame.grid_rowconfigure(i, weight=1)
        for i in range(5):  # 5 columns
            buttons_frame.grid_columnconfigure(i, weight=1)
        
        # --- Button Definitions with Icons ---
        buttons = [
            # Row 0 - Scientific functions
            ('sin', 0, 0, 'function', 'sin'), ('cos', 0, 1, 'function', 'cos'), 
            ('tan', 0, 2, 'function', 'tan'), ('log', 0, 3, 'function', 'log'), 
            ('ln', 0, 4, 'function', 'ln'),
            
            # Row 1 - More functions
            ('(', 1, 0, 'operator', '('), (')', 1, 1, 'operator', ')'), 
            ('√', 1, 2, 'function', '√'), ('x²', 1, 3, 'function', 'x²'), 
            ('^', 1, 4, 'operator', '^'),
            
            # Row 2 - Numbers and clear
            ('7', 2, 0, 'number', '7'), ('8', 2, 1, 'number', '8'), 
            ('9', 2, 2, 'number', '9'), ('⌫', 2, 3, 'operator', '⌫'), 
            ('C', 2, 4, 'operator', 'C'),
            
            # Row 3 - Numbers and operators
            ('4', 3, 0, 'number', '4'), ('5', 3, 1, 'number', '5'), 
            ('6', 3, 2, 'number', '6'), ('×', 3, 3, 'operator', '*'), 
            ('÷', 3, 4, 'operator', '/'),
            
            # Row 4 - Numbers and operators
            ('1', 4, 0, 'number', '1'), ('2', 4, 1, 'number', '2'), 
            ('3', 4, 2, 'number', '3'), ('+', 4, 3, 'operator', '+'), 
            ('−', 4, 4, 'operator', '-'),
            
            # Row 5 - Numbers and equals
            ('0', 5, 0, 'number', '0'), ('.', 5, 1, 'number', '.'), 
            ('π', 5, 2, 'function', 'π'), ('%', 5, 3, 'operator', '%'), 
            ('=', 5, 4, 'equals', '='),
            
            # Row 6 - Additional functions
            ('±', 6, 0, 'operator', '±'), ('1/x', 6, 1, 'function', '1/x'), 
            ('x³', 6, 2, 'function', 'x³'), ('10ˣ', 6, 3, 'function', '10ˣ'), 
            ('eˣ', 6, 4, 'function', 'eˣ')
        ]
        
        # --- Create and Place Buttons ---
        button_font = ctk.CTkFont(family="Arial", size=16, weight="bold")
        
        for (display_text, row, col, btn_type, action_text) in buttons:
            # Get icon for the button
            icon = self.icon_generator.get_icon(display_text, btn_type)
            icon_tk = self._pil_to_photoimage(icon)
            
            # Define colors based on button type
            if btn_type == 'number':
                fg_color = "#5F6368"
                hover_color = "#7F8388"
            elif btn_type == 'function':
                fg_color = "#34A853"
                hover_color = "#4CAF50"
            elif btn_type == 'operator':
                fg_color = "#EA4335"
                hover_color = "#F44336"
            elif btn_type == 'equals':
                fg_color = "#4285F4"
                hover_color = "#62A5F4"
            else:
                fg_color = "#343638"
                hover_color = "#4E5053"
            
            # Create button with icon and text
            button = ctk.CTkButton(buttons_frame,
                                   text=display_text,
                                   font=button_font,
                                   image=icon_tk,
                                   compound="top",
                                   command=lambda t=action_text: self._on_button_press(t),
                                   fg_color=fg_color,
                                   hover_color=hover_color,
                                   corner_radius=12,
                                   height=60)
            button.grid(row=row, column=col, padx=4, pady=4, sticky="nsew")
            
            # Store the icon reference to prevent garbage collection
            button.icon = icon_tk
        
        # --- History Display ---
        history_frame = ctk.CTkFrame(self, height=100, corner_radius=10)
        history_frame.grid(row=3, column=0, columnspan=2, padx=15, pady=10, sticky="ew")
        history_frame.grid_columnconfigure(0, weight=1)
        
        history_label = ctk.CTkLabel(history_frame, text="📋 History", 
                                   font=ctk.CTkFont(size=14, weight="bold"))
        history_label.grid(row=0, column=0, padx=10, pady=5, sticky="w")
        
        self.history_text = ctk.CTkTextbox(history_frame, height=60, 
                                          font=ctk.CTkFont(size=12))
        self.history_text.grid(row=1, column=0, padx=10, pady=5, sticky="ew")
    
    def _on_button_press(self, char):
        """Handles button presses with enhanced functionality."""
        if self.is_result_displayed:
            if char in ['+', '-', '*', '/', '^', '%']:
                current_expression = self.expression_var.get()
                self.expression_var.set(current_expression + char)
            else:
                self.expression_var.set(char)
            self.is_result_displayed = False
        else:
            # Handle special functions
            if char in ['sin', 'cos', 'tan', 'log', 'ln', '√']:
                self.expression_var.set(self.expression_var.get() + f"{char}(")
            elif char == 'x²':
                self.expression_var.set(self.expression_var.get() + "**2")
            elif char == 'x³':
                self.expression_var.set(self.expression_var.get() + "**3")
            elif char == '^':
                self.expression_var.set(self.expression_var.get() + "**")
            elif char == 'π':
                self.expression_var.set(self.expression_var.get() + "pi")
            elif char == '%':
                self.expression_var.set(self.expression_var.get() + "*0.01")
            elif char == '±':
                self._toggle_sign()
            elif char == '1/x':
                self._calculate_reciprocal()
            elif char == '10ˣ':
                self.expression_var.set(self.expression_var.get() + "10**")
            elif char == 'eˣ':
                self.expression_var.set(self.expression_var.get() + "math.e**")
            else:
                self.expression_var.set(self.expression_var.get() + char)
    
    def _toggle_sign(self):
        """Toggles the sign of the current number."""
        current = self.expression_var.get()
        if current and current != "Error":
            if current.startswith('-'):
                self.expression_var.set(current[1:])
            else:
                self.expression_var.set('-' + current)
    
    def _calculate_reciprocal(self):
        """Calculates the reciprocal of the current expression."""
        try:
            current = self.expression_var.get()
            if current and current != "Error":
                result = 1 / eval(current)
                self.expression_var.set(str(result))
                self.is_result_displayed = True
        except:
            self.expression_var.set("Error")
    
    def _calculate_result(self):
        """Evaluates the expression with enhanced error handling."""
        try:
            expression = self.expression_var.get()
            if not expression or expression == "Error":
                return
            
            # Add to history
            self._add_to_history(expression)
            
            # Replace user-friendly names with math module equivalents
            safe_expression = expression.replace('sin', 'math.sin')
            safe_expression = safe_expression.replace('cos', 'math.cos')
            safe_expression = safe_expression.replace('tan', 'math.tan')
            safe_expression = safe_expression.replace('log', 'math.log10')
            safe_expression = safe_expression.replace('ln', 'math.log')
            safe_expression = safe_expression.replace('√', 'math.sqrt')
            safe_expression = safe_expression.replace('pi', 'math.pi')
            
            # Evaluate the expression
            result = eval(safe_expression)
            
            # Format result
            if isinstance(result, (int, float)):
                if result == int(result):
                    result = int(result)
                else:
                    result = round(result, 8)
            
            self.expression_var.set(str(result))
            self.is_result_displayed = True
            
        except Exception as e:
            self.expression_var.set("Error")
            print(f"Calculation Error: {e}")
    
    def _add_to_history(self, expression: str):
        """Adds calculation to history."""
        self.history.append(expression)
        if len(self.history) > 10:  # Keep only last 10 entries
            self.history.pop(0)
        
        # Update history display
        self.history_text.delete("1.0", tk.END)
        for entry in self.history[-5:]:  # Show last 5 entries
            self.history_text.insert(tk.END, f"{entry}\n")
    
    def _clear_all(self):
        """Clears the display."""
        self.expression_var.set("")
        self.is_result_displayed = False
    
    def _backspace(self):
        """Removes the last character."""
        if self.is_result_displayed:
            self._clear_all()
        else:
            current = self.expression_var.get()
            if current:
                self.expression_var.set(current[:-1])
    
    def _toggle_theme(self):
        """Toggles between light and dark themes."""
        current_mode = ctk.get_appearance_mode()
        new_mode = "light" if current_mode == "dark" else "dark"
        ctk.set_appearance_mode(new_mode)

def main():
    """Main function to run the calculator."""
    app = ModernScientificCalculator()
    app.mainloop()

if __name__ == "__main__":
    main()