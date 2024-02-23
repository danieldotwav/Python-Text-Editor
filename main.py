import tkinter as tk
from tkinter import filedialog, Text, Menu

# Main Window

root = tk.Tk()
root.title("Python Text Editor")

# Features

class LineNumberCanvas(tk.Canvas):
    def __init__(self, *args, **kwargs):
        tk.Canvas.__init__(self, *args, **kwargs)
        self.textwidget = None

    def attach(self, text_widget):
        self.textwidget = text_widget

    def redraw(self, *args):
        '''Redraw line numbers'''
        self.delete("all")

        i = self.textwidget.index("@0,0")
        while True :
            dline= self.textwidget.dlineinfo(i)
            if dline is None: break
            y = dline[1]
            linenum = str(i).split(".")[0]
            self.create_text(2,y,anchor="nw", text=linenum)
            i = self.textwidget.index("%s+1line" % i)

def toggle_line_numbers():
    if line_numbers.winfo_ismapped():
        line_numbers.pack_forget()
        text.pack(side="right", fill="both", expand=True)  # Make sure the text widget expands to fill the space
    else:
        line_numbers.pack(side="left", fill="y")
        text.pack(side="right", fill="both", expand=True)  # Re-pack the text widget to maintain the layout
        line_numbers.redraw()  # Redraw the line numbers after showing the canvas

def new_file():
    text.delete(1.0, tk.END)
    line_numbers.redraw()  # Reset Numbers

def open_file():
    file_path = filedialog.askopenfilename(filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "r") as file:
            text.delete(1.0, tk.END)
            text.insert(tk.END, file.read())

def save_file():
    file_path = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text Files", "*.txt")])
    if file_path:
        with open(file_path, "w") as file:
            file.write(text.get(1.0, tk.END))

def select_all():
    text.tag_add('sel', '1.0', 'end')

def copy():
    if text.tag_ranges('sel'):
        text.clipboard_clear()
        text.clipboard_append(text.get(tk.SEL_FIRST, tk.SEL_LAST))

def paste():
    try:
        selected_text = text.selection_get(selection='CLIPBOARD')
        if text.tag_ranges('sel'):
            # If there's selected text, replace it with clipboard contents
            start = text.index(tk.SEL_FIRST)
            end = text.index(tk.SEL_LAST)
            text.delete(start, end)
            text.insert(start, selected_text)
        else:
            # If there's no selected text, just insert at the current position
            text.insert(tk.INSERT, selected_text)
    except tk.TclError:
        pass # Catch the exception if there's no text in the clipboard

def cut():
    if text.tag_ranges('sel'):
        copy()
        text.delete(tk.SEL_FIRST, tk.SEL_LAST)

# Custom Find and Replace Dialog Box
class FindReplaceDialog(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Find and Replace")

        # Find field
        self.find_label = tk.Label(self, text="Find:")
        self.find_label.grid(row=0, column=0, padx=10, pady=5)
        self.find_entry = tk.Entry(self)
        self.find_entry.grid(row=0, column=1, padx=10, pady=5)

        # Replace field
        self.replace_label = tk.Label(self, text="Replace with:")
        self.replace_label.grid(row=1, column=0, padx=10, pady=5)
        self.replace_entry = tk.Entry(self)
        self.replace_entry.grid(row=1, column=1, padx=10, pady=5)

        # Replace button
        self.replace_button = tk.Button(self, text="Replace", command=self.replace)
        self.replace_button.grid(row=2, column=0, padx=10, pady=5)

        # Cancel button
        self.cancel_button = tk.Button(self, text="Cancel", command=self.destroy)
        self.cancel_button.grid(row=2, column=1, padx=10, pady=5)

    def replace(self):
        find_text = self.find_entry.get()
        replace_text = self.replace_entry.get()
        if find_text and replace_text:
            content = text.get(1.0, tk.END)
            new_content = content.replace(find_text, replace_text)
            text.delete(1.0, tk.END)
            text.insert(1.0, new_content)
        self.destroy()

def open_find_replace_dialog():
    dialog = FindReplaceDialog(root)
    root.wait_window(dialog)  # This will wait until the dialog window is closed.

def add_shortcut(key, func):
    root.bind(key, lambda event: func())


#### Dark Mode Feature ####

# Color schemes
light_mode = {
    "text_bg": "#FFFFFF",  # White background for the text area
    "text_fg": "#000000",  # Black text color
    "sidebar_bg": "#F0F0F0",  # Light background for line numbers
    "sidebar_fg": "#000000",  # Black color for line numbers
    "menu_bg": "#F0F0F0",  # Light background for the menu
    "menu_fg": "#000000",  # Black text color for the menu
}

dark_mode = {
    "text_bg": "#333333",  # Dark background for the text area
    "text_fg": "#CCCCCC",  # Light grey text color
    "sidebar_bg": "#1E1E1E",  # Dark background for line numbers
    "sidebar_fg": "#FFFFFF",  # White color for line numbers
    "menu_bg": "#1E1E1E",  # Dark background for the menu
    "menu_fg": "#CCCCCC",  # Light grey text color for the menu
}

# Current mode starts as light mode
current_mode = "light"

def toggle_dark_mode():
    global current_mode
    # Toggle between 'light' and 'dark'
    current_mode = 'dark' if current_mode == 'light' else 'light'
    color_scheme = dark_mode if current_mode == 'dark' else light_mode
    
    # Apply color scheme to text widget and line numbers
    text.config(bg=color_scheme["text_bg"], fg=color_scheme["text_fg"], insertbackground=color_scheme["text_fg"])
    line_numbers.config(bg=color_scheme["sidebar_bg"], fg=color_scheme["sidebar_fg"])
    
    # Update the colors for the menu and all of its children
    menu.config(bg=color_scheme["menu_bg"], fg=color_scheme["menu_fg"])
    for menu_item in menu.winfo_children():
        menu_item.config(bg=color_scheme["menu_bg"], fg=color_scheme["menu_fg"])

# Bind shortcuts to these functions

add_shortcut('<Control-n>', new_file)
add_shortcut('<Control-o>', open_file)
add_shortcut('<Control-s>', save_file)
add_shortcut('<Control-a>', select_all)
add_shortcut('<Control-f>', open_find_replace_dialog)
add_shortcut('<Control-x>', cut)
add_shortcut('<Control-c>', copy)
add_shortcut('<Control-v>', paste)
add_shortcut('<Control-l>', toggle_line_numbers)

# File Menu

menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file, accelerator="Ctrl+N")
file_menu.add_command(label="Open", command=open_file, accelerator="Ctrl+O")
file_menu.add_command(label="Save", command=save_file, accelerator="Ctrl+S")
file_menu.add_separator()

file_menu.add_command(label="Toggle Line Numbers", command=toggle_line_numbers, accelerator="Ctrl+L")
file_menu.add_separator()

file_menu.add_command(label="Exit", command=root.quit)

# Edit Menu

edit_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="Edit", menu=edit_menu)
edit_menu.add_command(label="Undo", command=lambda: text.edit_undo(), accelerator="Ctrl+Z")
edit_menu.add_command(label="Redo", command=lambda: text.edit_redo(), accelerator="Ctrl+Y")
edit_menu.add_separator()

edit_menu.add_command(label="Cut", command=cut, accelerator="Ctrl+X")
edit_menu.add_command(label="Copy", command=copy, accelerator="Ctrl+C")
edit_menu.add_command(label="Paste", command=paste, accelerator="Ctrl+V")
edit_menu.add_separator()

edit_menu.add_command(label="Select All", command=select_all, accelerator="Ctrl+A")
edit_menu.add_command(label="Find and Replace", command=open_find_replace_dialog, accelerator="Ctrl+F")

# View Menu

view_menu = tk.Menu(menu, tearoff=0)
menu.add_cascade(label="View", menu=view_menu)
view_menu.add_command(label="Toggle Dark Mode", command=toggle_dark_mode)

# Line Numbers
line_numbers = LineNumberCanvas(root, width=30)
line_numbers.pack(side="left", fill="y")

# Text Area
text = tk.Text(root, wrap=tk.WORD)
text.pack(expand=True, fill="both")

# Enable Undo/Redo Feature
text.config(undo=True)

# Attach text widget to line numbers
line_numbers.attach(text)

# Initial redraw to display line number 1 before typing
line_numbers.redraw()

# Redraw line numbers on text change
text.bind("<KeyRelease>", lambda event: line_numbers.redraw())
text.bind("<MouseWheel>", lambda event: line_numbers.redraw())

# GUI Main Loop
root.mainloop()