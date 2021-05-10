# Cox Orb Data Analyzers

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, FigureCanvasAgg
from matplotlib import pyplot as plt
import numpy as np
import PySimpleGUI as sg

from src import layout

def draw_figure(canvas, fig):
    if canvas.children:
        for child in canvas.winfo_children():
            child.destroy()
    figure_canvas_agg = FigureCanvasTkAgg(fig, master=canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='right', fill='both', expand=1)

def main():

    sg.theme(layout.THEME)

    # Create the Window
    window = sg.Window('CODA', layout.layout, size=layout.SIZE)
    window.finalize()

    # Event Loop to process "events" and get the "values" of the inputs
    while True:
        event, values = window.read()
        if event == sg.WIN_CLOSED: # if user closes window
            break
        elif event == 'TEST':

            plt.figure(1)
            fig = plt.gcf()
            DPI = fig.get_dpi()
            # ------------------------------- you have to play with this size to reduce the movement error when the mouse hovers over the figure, it's close to canvas size
            fig.set_size_inches(700 / float(DPI), 500 / float(DPI))
            # -------------------------------
            x = np.linspace(0, 2 * np.pi)
            y = np.sin(x)
            plt.plot(x, y)
            plt.title('y=sin(x)')
            plt.xlabel('X')
            plt.ylabel('Y')
            plt.grid('on')

            # ------------------------------- Instead of plt.show()
            draw_figure(window['CANVAS'].TKCanvas, fig)

    window.close()