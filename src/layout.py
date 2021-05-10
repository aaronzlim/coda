# A module for the layout of the application.

import PySimpleGUI as sg

THEME: str = 'Dark'
SIZE = (1020, 640)
FONT = ('Cambria', 14)

layout = [
    [
        sg.Button('Load GPX File   ', key='GPX_BUTTON', font=FONT),
        sg.InputText(size=(40,1), key='GPX_INPUTTEXT', font=FONT),
    ],
    [
        sg.Button('Load Graph File', key='GRAPH_BUTTON', font=FONT),
        sg.InputText(size=(40,1), key='GRAPH_INPUTTEXT', font=FONT),
    ],
    [
        sg.Canvas(size=(500, 500), key='CANVAS_GPX'),
        sg.Canvas(size=(500, 500), key='CANVAS_GRAPH'),
    ],
]