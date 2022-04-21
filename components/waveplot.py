import tkinter as tk
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


class Waveplot:

    def __init__(self, master, N=100, figsize = (6,5)) -> None:
        
        self.phi = 0

        fig = Figure(figsize=(8, 6))
        self._axes = fig.add_subplot(111)
        self._axes.set_ylim(-1.05,1.05)

        self._canvas = FigureCanvasTkAgg(fig, master=master)  # A tk.DrawingArea.
        self._canvas.draw()
        self._line = None
        self._N = 100

        self._wave = np.zeros(self._N)
        self._wavetype = tk.StringVar(value='sin')
        self.draw()

    def draw(self):
        if self._line is None:
            self._line = self._axes.plot(self._wave)[0]
        else:
            self._line.set_ydata(self._wave)
        self._canvas.draw()
    
    @property
    def widget(self):
        return self._canvas.get_tk_widget()
    
    @property
    def wavetype(self):
        return self._wavetype    

    def update(self, dt):
        self.phi += 5e-3*dt
        self.calculate_wave()
        self.draw()

    def calculate_wave(self):

        phi = (np.linspace(0, 2*np.pi, 100)+self.phi)%(2*np.pi)

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

