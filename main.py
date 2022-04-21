import numpy as np
import tkinter as tk
from tkinter import ttk
from ctypes import windll
from components.waveplot import Waveplot

class DemoApp(tk.Tk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        # Uncomment this line to have a sharper but smaller GUI
        # windll.shcore.SetProcessDpiAwareness(1)
        self.title('Oscilloscope demo')
        #self.geometry('1024x768')
        self.tk.call('tk', 'scaling', 1.5)

        self._mainframe = ttk.Frame(self, padding='3 3 12 12')
        self._mainframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=5)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(0, weight=4)
        self.mainframe.rowconfigure(1, weight=1)

        self._dt = 40

        self._wplot = Waveplot(self.mainframe, figsize=(8,6))
        self._wplot.widget.grid(column=0, row=0, padx=10, pady=10)

        self._radios = ttk.Labelframe(master=self.mainframe, text='Wave type', padding='10')
        self._radios.grid(column=1, row=0, padx=10, pady=10, sticky=(tk.N, tk.S, tk.W, tk.E))

        wtype = self._wplot.wavetype

        ttk.Radiobutton(self._radios, text='Sine', value='sin', variable=wtype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Square', value='sqr', variable=wtype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Triangle', value='tri', variable=wtype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Sawtooth', value='saw', variable=wtype).pack(fill='x')

        self._playbar = ttk.Frame(master=self.mainframe)
        self._playbar.grid(column=0, row=1, columnspan=2, padx=10, pady=10)     

        self._playing = True

        ttk.Button(self._playbar, text='Play',  command=self.play).pack(side=tk.LEFT)
        ttk.Button(self._playbar, text='Pause', command=self.pause).pack(side=tk.LEFT)
        ttk.Button(self._playbar, text='Stop',  command=self.stop).pack(side=tk.LEFT)

        self.after(self._dt, self.update_wave)

    @property
    def mainframe(self) -> ttk.Frame:
        return self._mainframe

    def play(self):
        self._playing = True

    def pause(self):
        self._playing = False
    
    def stop(self):
        self.pause()
        self._phi = 0
        self.redraw()

    def redraw(self):
        self.calculate_wave()
        self._sinline.set_ydata(self._wave)
        self._canvas.draw()
    
    def update_wave(self) -> None:

        if self._playing:
            self._wplot.update(self._dt)

        self.after(self._dt, self.update_wave)

if __name__ == '__main__':

    app = DemoApp()
    app.mainloop()