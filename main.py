from functools import update_wrapper
from turtle import update
import numpy as np
import tkinter as tk
from tkinter import ttk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class DemoApp(tk.Tk):

    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)

        self.title('Oscilloscope demo')

        self._mainframe = ttk.Frame(self, padding='3 3 12 12')
        self._mainframe.grid(column=0, row=0, sticky=(tk.N, tk.S, tk.W, tk.E))
        self.columnconfigure(0, weight=1)
        self.rowconfigure(0, weight=1)

        self.mainframe.columnconfigure(0, weight=5)
        self.mainframe.columnconfigure(1, weight=1)
        self.mainframe.rowconfigure(0, weight=4)
        self.mainframe.rowconfigure(1, weight=1)

        fig = Figure(figsize=(5, 4), dpi=100)
        self._phi = 0
        self._dt = 40

        self._canvas = FigureCanvasTkAgg(fig, master=self.mainframe)  # A tk.DrawingArea.
        self._canvas.draw()
        self._canvas.get_tk_widget().grid(column=0, row=0)

        self._radios = ttk.Labelframe(master=self.mainframe, text='Wave type', padding='10')
        self._radios.grid(column=1, row=0)

        self._wavetype = tk.StringVar(value='sin')

        ttk.Radiobutton(self._radios, text='Sine', value='sin', variable=self._wavetype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Square', value='sqr', variable=self._wavetype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Triangle', value='tri', variable=self._wavetype).pack(fill='x')
        ttk.Radiobutton(self._radios, text='Sawtooth', value='saw', variable=self._wavetype).pack(fill='x')

        self._playbar = ttk.Frame(master=self.mainframe)
        self._playbar.grid(column=0, row=1, columnspan=2)       

        self._playing = True

        ttk.Button(self._playbar, text='Play',  command=self.play).pack(side=tk.LEFT)
        ttk.Button(self._playbar, text='Pause', command=self.pause).pack(side=tk.LEFT)
        ttk.Button(self._playbar, text='Stop',  command=self.stop).pack(side=tk.LEFT)

        self.calculate_wave()
        self._sinline = fig.add_subplot(111).plot(self._wave)[0]

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

    def calculate_wave(self):

        phi = (np.linspace(0, 2*np.pi, 100)+self._phi)%(2*np.pi)

        wave_type = self._wavetype.get()
        
        if wave_type == 'sin':
            wave = np.sin(phi)
        elif wave_type == 'sqr':
            wave = np.where(phi < np.pi, 1.0, -1.0)
        elif wave_type == 'tri':
            t1 = phi*2/np.pi
            t2 = 2.0-t1
            t3 = t1-4.0
            wave = np.where(phi < np.pi/2.0, t1, np.where(phi < 1.5*np.pi, t2, t3))
        elif wave_type == 'saw':
            wave = phi/np.pi-1.0
        else:
            # Just do nothing
            wave = phi*0.0
        
        self._wave = wave
    
    def update_wave(self) -> None:

        if self._playing:
            self._phi += self._dt/1e3*5
            self.redraw()

        self.after(self._dt, self.update_wave)

if __name__ == '__main__':

    app = DemoApp()
    app.mainloop()