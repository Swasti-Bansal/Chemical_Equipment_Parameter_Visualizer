from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

THEME_BG = "#111426"
GRID = "#262a40"
TEXT = "#cbd5e1"
COL_BLUE = "#6366f1"
COL_GREEN = "#34d399"
COL_ORANGE = "#fbbf24"
COL_RED = "#fb7185"
COL_LIGHT_BLUE = "#60a5fa"

class MplCanvas(FigureCanvas):
    def __init__(self):
        self.fig = Figure()
        self.ax = self.fig.add_subplot(111)
        super().__init__(self.fig)

        self.fig.patch.set_facecolor(THEME_BG)
        self.ax.set_facecolor(THEME_BG)
        self.ax.tick_params(colors=TEXT)
        for spine in self.ax.spines.values():
            spine.set_color(GRID)

    def _style(self, title: str):
        self.ax.set_title(title, color=TEXT, fontsize=11, fontweight="bold", pad=12)
        self.ax.grid(True, color=GRID, alpha=0.35, linewidth=0.8)
        self.ax.tick_params(colors=TEXT, labelsize=9)
        for spine in self.ax.spines.values():
            spine.set_color(GRID)

    def clear(self, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)
        self._style(title)
        self.draw()

    def bar(self, labels, values, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)

        if labels and values:
            palette = [COL_BLUE, COL_GREEN, COL_ORANGE, COL_RED, COL_LIGHT_BLUE]
            colors = [palette[i % len(palette)] for i in range(len(labels))]
            self.ax.bar(labels, values, color=colors, edgecolor=GRID, linewidth=0.8)
            self.ax.tick_params(axis="x", rotation=15)

        self._style(title)
        self.fig.tight_layout()
        self.draw()

    def lines(self, xlabels, series_dict, title=""):
        self.ax.clear()
        self.ax.set_facecolor(THEME_BG)

        colors = {
            "Flow": COL_GREEN,     
            "Pressure": COL_ORANGE,
            "Temp": COL_RED,        
        }

        for name, y in series_dict.items():
            if not y:
                continue
            
            valid_indices = [i for i, val in enumerate(y) if val is not None]
            if not valid_indices:
                continue
                
            valid_x = [xlabels[i] for i in valid_indices]
            valid_y = [y[i] for i in valid_indices]
            
            self.ax.plot(
                valid_x,
                valid_y,
                label=name,
                color=colors.get(name, COL_LIGHT_BLUE),
                linewidth=2.2,
                marker="o",
                markersize=4.5,
            )

        self._style(title)
        
        legend = self.ax.legend(
            facecolor=THEME_BG,
            edgecolor=GRID,
            labelcolor=TEXT,
            fontsize=9,
            loc='upper left'
        )
        legend.get_frame().set_linewidth(0.8)
        
        self.fig.tight_layout()
        self.draw()