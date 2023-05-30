import sys
sys.path.append('..')
import numpy as np
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
from util import SampleRate

class PlotComponent:
    def __init__(self,
                 column: int,
                 row: int,
                 padx: int,
                 pady: int,
                 fig_title: str,
                 wave_color: str,
                 parent):
        
        self.parent = parent

        self.fig_title = fig_title
        self.wave_color = wave_color
        self.column = column
        self.row = row
        self.padx = padx
        self.pady = pady

    def update_plot(self,
                    buff: np.ndarray,
                    plot_len_s: float,
                    sr: SampleRate) -> None:
        
        if type(buff) == np.ndarray:
            xlim = int(plot_len_s * sr.value)
            self.fig = Figure(figsize = (2.5, 1.5),
                              dpi = 100)
            self.fig.suptitle(self.fig_title, color='white')
            # first channel
            left = self.fig.add_subplot(211)
            left.plot(buff[0], color=self.wave_color)
            left.set_ylim([-1, 1])
            left.set_xlim([0, xlim])
            left.axis('off')
            # second channel
            right = self.fig.add_subplot(212)
            right.plot(buff[1], color=self.wave_color)
            right.set_ylim([-1, 1])
            right.set_xlim([0, xlim])
            right.axis('off')
            # show
            self.fig.set_facecolor('black')
            self.fig.tight_layout(pad=0.25)
            self.fig.subplots_adjust(top=0.85)

            self.canvas = FigureCanvasTkAgg(self.fig,
                                            master = self.parent)
            self.canvas.draw()

            self.canvas.get_tk_widget().grid(column=self.column, row=self.row, padx=self.padx, pady=self.pady)