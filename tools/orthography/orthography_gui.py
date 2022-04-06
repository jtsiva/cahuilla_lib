#!/usr/bin/python3

from tkinter import *
import json
from functools import partial
import orthography

class MainWindow():
    def __init__(self):
        self.root = Tk()
        self.root.winfo_toplevel().title("Cahuilla Orthography")

        self.input_output_frame = Frame (self.root)
        self.input_output_frame.pack(side=BOTTOM)

        self.input_text = Text(self.input_output_frame, width=60)
        self.input_text.pack(side = LEFT)
        self.output_text = Text(self.input_output_frame, state='disabled', width=60)
        self.output_text.pack(side=RIGHT)

        self.convert_button = Button(self.input_output_frame, text = '>>>', command=self.convert_orthography)
        self.convert_button.pack(side = RIGHT)

        self.ortho = orthography.Orthography('../../sounds/orthography.json')
        

        for ortho_name, chars in self.ortho.orthography_dict.items():
            self.create_orthography_buttons(self.root, ortho_name.split('_')[0], chars)

    def update_input_text(self, char):
        self.input_text.insert(END, char)

    def create_orthography_buttons(self, parent, title, characters):
        ortho_frame = Frame(parent)
        ortho_frame.pack(side = TOP)
        label = Label(ortho_frame, text = title)
        label.pack (side = LEFT)

        for char in characters:
            btn = Button(ortho_frame, text = char, command = partial(self.update_input_text, char))
            btn.pack(side = LEFT)


    def convert_orthography(self):
        self.output_text.configure(state=NORMAL)
        self.output_text.delete("1.0", END)
        self.output_text.insert(END, self.ortho.convert_orthography(self.input_text.get("1.0",END).strip()))
        self.output_text.configure(state=DISABLED)

    def run(self):
        self.root.mainloop()

def main():
    window = MainWindow()
    window.run()

if __name__ == '__main__':
    main()
