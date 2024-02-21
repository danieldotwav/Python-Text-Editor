import tkinter as tk
from tkinter import filedialog

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

# Main Window
root = tk.Tk()
root.title("Python Text Editor")

# Menu
menu = tk.Menu(root)
root.config(menu=menu)

file_menu = tk.Menu(menu)
menu.add_cascade(label="File", menu=file_menu)
file_menu.add_command(label="New", command=new_file)
file_menu.add_command(label="Open", command=open_file)
file_menu.add_command(label="Save", command=save_file)
file_menu.add_separator()
file_menu.add_command(label="Toggle Line Numbers", command=toggle_line_numbers)  # Toggle line numbers
file_menu.add_command(label="Exit", command=root.quit)

# Line Numbers
line_numbers = LineNumberCanvas(root, width=30)
line_numbers.pack(side="left", fill="y")

# Text Area
text = tk.Text(root, wrap=tk.WORD)
text.pack(expand=True, fill="both")

# Attach text widget to line numbers
line_numbers.attach(text)

# Redraw line numbers on text change
text.bind("<KeyRelease>", lambda event: line_numbers.redraw())
text.bind("<MouseWheel>", lambda event: line_numbers.redraw())

# GUI Main Loop
root.mainloop()
