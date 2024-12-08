import tkinter as tk
from tkinter import ttk

class AttractionView:
    def __init__(self, root):
        self.root = root
        self.root.title("Attraction Selector")

        # Widgets for category selection
        self.category_label = tk.Label(root, text="Choose a category:")
        self.category_label.pack(pady=5)

        self.category_var = tk.StringVar(value="Select a category")
        self.category_menu = ttk.OptionMenu(root, self.category_var, "Select a category")
        self.category_menu.pack(pady=5)

        # Widgets for attraction selection
        self.attraction_label = tk.Label(root, text="Choose an attraction:")
        self.attraction_label.pack(pady=5)

        self.attraction_var = tk.StringVar(value="Select an attraction")
        self.attraction_menu = ttk.OptionMenu(root, self.attraction_var, "Select an attraction")
        self.attraction_menu.pack(pady=5)

        # Display selection button
        self.display_button = tk.Button(root, text="Display Selection")
        self.display_button.pack(pady=10)

    def set_category_options(self, options):
        self.category_menu['menu'].delete(0, 'end')
        for option in options:
            self.category_menu['menu'].add_command(label=option, command=tk._setit(self.category_var, option))

    def set_attraction_options(self, options):
        self.attraction_menu['menu'].delete(0, 'end')
        for option in options:
            self.attraction_menu['menu'].add_command(label=option, command=tk._setit(self.attraction_var, option))

    def get_selected_category(self):
        return self.category_var.get()

    def get_selected_attraction(self):
        return self.attraction_var.get()

    def set_display_button_action(self, action):
        self.display_button.config(command=action)
