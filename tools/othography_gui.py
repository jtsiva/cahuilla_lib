#!/usr/bin/python3

from tkinter import *
import json
from functools import partial

def create_output_text (parent):
    text_output = Text (parent)
    text_output.pack(side=BOTTOM)
    def button_press (char):
        text_output.insert(END, char)

    return button_press


def create_orthography_buttons(parent, title, characters, button_action):
    ortho_frame = Frame(parent)
    ortho_frame.pack(side = TOP)
    label = Label(ortho_frame, text = title)
    label.pack (side = LEFT)

    for char in characters:
        btn = Button(ortho_frame, text = char, command = partial(button_action, char))
        btn.pack(side = LEFT)

def main():
    root = Tk()
    root.winfo_toplevel().title("Cahuilla Orthography")
    output_text_update = create_output_text(root)
    
    ortho_dict = {}
    with open ('../sounds/orthography.json') as file:
        ortho_dict = json.load(file)

    for ortho_name, chars in ortho_dict.items():
        create_orthography_buttons(root, ortho_name.split('_')[0], chars, output_text_update)

    # Code to add widgets will go here...
    root.mainloop()

if __name__ == '__main__':
    main()