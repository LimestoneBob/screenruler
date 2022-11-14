import tkinter as tk
import tkinter.ttk as ttk
import itertools
from conversions import CONVERSIONS
import sys
import os

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    base_path = getattr(sys, '_MEIPASS', os.path.dirname(os.path.abspath(__file__)))
    return os.path.join(base_path, relative_path)

resource_path('conversions')
resource_path('favicon.ico')

class Popup(tk.Menu):
    def __init__(self, *args, **kwargs):
        """Adapted from http://effbot.org/zone/tkinter-popup-menu.htm"""
        tk.Menu.__init__(self, *args, **kwargs)

    def do_popup(self, event):
        # display the popup menu
        try:
            self.tk_popup(event.x_root, event.y_root, 0)
        finally:
            # make sure to release the grab (Tk 8.0a1 only)
            # self.grab_release()
            pass

class window_tosetscale(tk.Toplevel):
    # https://www.pythontutorial.net/tkinter/tkinter-toplevel/
    
    def __init__(self, parent):
        super().__init__(parent)
        
        self.geometry("290x60")
        self.title('Set scale factor')
        self.iconbitmap(r'E:\screenrulerWin\favicon.ico')

        # Define Widgets
        self.configure(bg = 'yellow2')

        label = tk.Label(self, text="unit multiplier: ", bg='yellow2')
        label.grid(row=0, column=0, sticky="e", pady=15)       

        self.entry = ttk.Entry(self, width=10)
        self.entry.grid(row=0, column=1, sticky="w")
        
        self.metric = tk.StringVar(self)
        self.metric.set("ft") # default value
        m = ttk.OptionMenu(self, self.metric, "ft", "mm")
        m.grid(row=0, column=2)
        
        button = ttk.Button(self, text="Done", command=self.getvalue)
        button.grid(row=0, column=3, sticky="w")
        
    # set window over root window
    def win_pos(self, xcoord, ycoord):
        x = xcoord
        y = ycoord
        # new window relative to the root window
        self.geometry("+%d+%d" %(x-80+200,y-60+60))

    def getvalue(self):
        # pass scale value to parent,App
        # Validation of user input required. Check for number. 
        if (self.entry.get().isdigit()):
            App.scale_value = int(self.entry.get())
            App.unitMeasure = self.metric.get()
        try:
            float(self.entry.get())
            App.scale_value = float(self.entry.get())
            App.unitMeasure = self.metric.get()
        except:
            pass 
        #close menu    
        self.destroy()
        

class App(tk.Tk):
    scale_value = 0 # user input; scale multiplier
    unitMeasure = "ft"
    unitMulti = 0 # unit scaled to correct measure
    cntTime = 0 # use to keep time for display of scaled unit

    def __init__(self, *args, **kwargs):
        super().__init__()
        self.dpi = self.winfo_fpixels('1m')
        self.title("Ruler")

        self.iconbitmap(r'E:\screenrulerWin\favicon.ico')

        # Define Widgets
        self.frame = tk.Frame(self)
        self.canvas = tk.Canvas(self.frame)
        self.frame.pack(side='bottom', fill='both', expand=True)
        self.canvas.pack(side='bottom', fill='both', expand=True)
        self.canvas['background'] = 'yellow2'
        
        # Define transparency
        # https://stackoverflow.com/questions/19080499/transparent-background-in-a-tkinter-window
        self.attributes("-alpha", 0.8)

        # Allow user to move window by dragging it
        self.bind("<ButtonPress-1>", self.start_window_move)
        self.bind("<ButtonRelease-1>", self.stop_window_move)
        self.bind("<B1-Motion>", self.on_window_move)

        # Select unit of measure to convert
        self.bind("<Double-Button-1>", self.unitConv)

        # Define Dimensions
        self._orient = 'horizontal'  # Orientation of ruler
        self._maxsize = 100  # Width of the ruler
        self._tickside = 'bottom'  # Side of the ruler ticks are drawn on
        self._measure = 'px'  # Measure used by the ruler
        self._measure_tick_positions = {
            'px': [50, 25, 5],
            'pt': [50, 10, 5],
            'em': [5, 1, .5],
            'in': [1, 0.5, 0.1],
            'mm': [10, 5, 1],
            'pi': [6, 3, 1]
        }

        # Create the menu
        self.popup_menu = Popup(self, tearoff=0)
        commands = [
            {"label": "Rotate", "command": self.rotate},
            {"label": "Pixels", "command": lambda *args: self.__dict__.update({"_measure": "px"})},
            {"label": "Points", "command": lambda *args: self.__dict__.update({"_measure": "pt"})},
            {"label": "Em", "command": lambda *args: self.__dict__.update({"_measure": "em"})},
            {"label": "Inches", "command": lambda *args: self.__dict__.update({"_measure": "in"})},
            {"label": "Millimeters", "command": lambda *args: self.__dict__.update({"_measure": "mm"})},
            {"label": "Picas", "command": lambda *args: self.__dict__.update({"_measure": "pi"})},
            {"label": "Scale*x", "command": self.open_scale_window},
        ]
        for cmd in commands:
            self.popup_menu.add_command(**cmd)
        self.canvas.bind("<Button-3>", self.popup_menu.do_popup)
        self.after(100, self.step)

    def step(self):
        self.update_dimensions()
        self.canvas.delete('all')
        self.update_orientation()
        self.draw_ticks()
        self.draw_reference_line()
        self.dispMeasure()
        self.after(50, self.step)

    def update_dimensions(self):
        self._width = self.winfo_width()
        self._height = self.winfo_height()

    def update_orientation(self):
        if self._orient == 'horizontal':
            self.maxsize(100000, self._maxsize)
        elif self._orient == 'vertical':
            self.maxsize(self._maxsize, 100000)
        else:
            raise ValueError("Orientation must be horizontal or vertical")

    def draw_ticks(self):
        # Get span of window in desired unit
        if self._tickside in ('bottom', 'top'):
            span_m = CONVERSIONS['px'][self._measure](self._width)
        else:
            span_m = CONVERSIONS['px'][self._measure](self._height)

        # For each of the offsets draw ticks in the desired positions
        ticks = map(
            lambda m: map(lambda c: m * c, itertools.count()),
            self._measure_tick_positions[self._measure]
        )

        for i, m in enumerate(ticks):
            while True:
                tick = next(m)
                tick_px = int(CONVERSIONS[self._measure]['px'](tick))
                if tick > span_m:
                    break
                if i == 0:
                    self.canvas.create_text(self.tick_coords(tick_px, 30)[:2], text=str(tick))
                elif i == 1:
                    self.canvas.create_line(*self.tick_coords(tick_px, 15))
                elif i == 2:
                    self.canvas.create_line(*self.tick_coords(tick_px, 5))

    def draw_reference_line(self):
        x, y = self.get_mouse_pos()
        if self._orient == "horizontal":
            x1, y1, x2, y2 = self.tick_coords(x, self._height - 20)
            self.canvas.create_line(x1, y1, x2, y2)
            text_offset = -10 if self._tickside == 'bottom' else 10
            self.canvas.create_text(
                x1, y1 + text_offset,
                text="{:.2f} {}".format(float(CONVERSIONS['px'][self._measure](x)), self._measure)
            )
        else:
            x1, y1, x2, y2 = self.tick_coords(y, self._width)
            self.canvas.create_line(x1, y1, x2, y2)
            self.canvas.create_text(
                0 if self._tickside == 'right' else self._width,
                y1 - 10,
                text="{:.2f} {}".format(float(CONVERSIONS['px'][self._measure](y)), self._measure),
                anchor='e' if self._tickside == 'left' else 'w'
            )

    def tick_coords(self, m, d):
        """
        Returns px coordinates for ticks drawn on the canvas.
        :param m: Measure the tick represents (m=6 for the 6px tick)
        :param d: Offset in px for the inside end of the tick
        :return: (x1, y1, x2, y2)
        """
        coords = {
            'bottom': (m, self._height - d, m, self._height),
            'top': (m, d, m, 0),
            'right': (self._width - d, m, self._width, m),
            'left': (d, m, 0, m),
        }
        return coords[self._tickside]

    def get_mouse_pos(self):
        abs_coord_x = self.winfo_pointerx() - self.winfo_rootx()
        abs_coord_y = self.winfo_pointery() - self.winfo_rooty()
        return abs_coord_x, abs_coord_y

    def rotate(self):
        w, h = self._height, self._width
        self._tickside = {"bottom": "right", "right": "top", "top": "left", "left": "bottom"}[self._tickside]
        self._orient = {"bottom": "horizontal", "right": "vertical", "top": "horizontal", "left": "vertical"}
        self._orient = self._orient[self._tickside]
        self.maxsize(10000, 10000)
        self.geometry("%dx%d"%(w, h))
        self.update_idletasks()

    # https://stackoverflow.com/questions/4055267/python-tkinter-mouse-drag-a-window-without-borders-eg-overridedirect1
    def start_window_move(self, event):
        self._x = event.x
        self._y = event.y

    def stop_window_move(self, event):
        self._x = None
        self._y = None

    def on_window_move(self, event):
        deltax = event.x - self._x
        deltay = event.y - self._y
        x = self.winfo_x() + deltax
        y = self.winfo_y() + deltay
        self.geometry("+%s+%s" % (x, y))
        
    def open_scale_window(self):
        # open new window for scale input relative to the root window
        x = self.winfo_x()
        y = self.winfo_y()
        window = window_tosetscale(self)
        window.win_pos(x, y)
        window.grab_set()

    def unitConv(self, event):
        # unit of measure conversion
        x, y = self.get_mouse_pos()
        if self._orient == "horizontal":
            self.unitMulti = self.scale_value*int(x)
        else:
            self.unitMulti = self.scale_value*int(y)

    def dispMeasure(self):
        x, y = self.get_mouse_pos()
        if self.unitMulti > 0:
            self.cntTime += 1
            if self.cntTime < 240:
                if self._orient == "horizontal":
                    self.canvas.create_text(x-40, y+5, text="{:.2f} {}".format(self.unitMulti, self.unitMeasure))
                else:
                    self.canvas.create_text(x+10, y+25, text="{:.2f} {}".format(self.unitMulti, self.unitMeasure))
            else:
                self.unitMulti = 0
                self.cntTime = 0
        
if __name__ == "__main__":
    app = App()
    app.mainloop()
