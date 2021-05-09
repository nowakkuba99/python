try:
    import Tkinter as tk
except ImportError:
    import tkinter as tk
import csv
import pandas as pd
import numpy as np

from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from matplotlib import pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.animation as animation

import random
import Algorythm
import Display_Func
import csv

answer = tk.IntVar()
ax = plt.axes(projection="3d")
X, Y, Z = [], [], []
lim_z = 0
best = 0


def increment(var):
    var.set(var.get() + 1)
    print(var.get())


class App(tk.Frame):
    def __init__(self, master=None, **kwargs):
        tk.Frame.__init__(self, master, **kwargs)

        self.running = False
        self.ani = None

        btns = tk.Frame(self)
        btns.pack()

        lbl = tk.Label(btns, text="Number of populations")
        lbl.pack(side=tk.LEFT)

        self.pop = tk.Entry(btns, width=5)
        self.pop.insert(0, '10')
        self.pop.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Number of candidates")
        lbl.pack(side=tk.LEFT)

        self.cans = tk.Entry(btns, width=5)
        self.cans.insert(0, '10')
        self.cans.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="update interval (ms)")
        lbl.pack(side=tk.LEFT)

        self.interval = tk.Entry(btns, width=5)
        self.interval.insert(0, '100')
        self.interval.pack(side=tk.LEFT)

        self.btn = tk.Button(btns, text='Start', command=self.on_click)
        self.btn.pack(side=tk.LEFT)

        self.fig = plt.Figure()
        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.line, = self.ax1.plot([], [], [], marker='o')
        # self.Disp_Opti_Func()
        # self.line, = self.ax1.plot([], [], 1, lw=2)
        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        # self.canvas.show()
        self.canvas.get_tk_widget().pack()

        self.ax1.set_ylim(0, 100)
        self.ax1.set_xlim(0, 100)
        #self.ax1.set_zlim(0, lim_z+0.1*lim_z)
        #self.ax1.set_zlim(0, 1)
        # self.ax1.tight_layout()

    def on_click(self):
        '''the button is a start, pause and unpause button all in one
        this method sorts out which of those actions to take'''
        self.ax1.cla()
        if self.ani is None:
            # animation is not running; start it
            return self.start()

        if self.running:
            # animation is running; pause it
            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            # animation is paused; unpause it
            self.ani.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

    def start(self):
        X, Y, Z = [], [], []
        algorytm = Algorythm.Talgorythm(
            int(self.cans.get()), int(self.pop.get()))
        algorytm.run()
        with open('test.csv', 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerows(Algorythm.list_of_rows)
        self.Read_data()
        self.ax1.cla()
        self.Disp_Opti_Func()
        self.points = int(self.pop.get()) + 1
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points,
            interval=int(self.interval.get()),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.ani._start()
        print('started animation')

    """def update_graph(self, i):
        self.line.set_data(*get_data())  # update graph

        if i >= self.points - 1:
            # code to limit the number of run times; could be left out
            self.btn.config(text='Start')
            self.running = False
            self.ani = None
        return self.line,"""

    def update_graph(self, i):
        if(i < int(self.pop.get())):
            # plot.plot(X[i], Y[i], Z[i], marker='o')
            self.ax1.scatter3D(X[i], Y[i], Z[i], marker='o')
        else:
            # code to limit the number of run times; could be left out
            self.btn.config(text='Start')
            self.running = False
            self.ani = None

    def Display_function(self, x_min, y_min, x_max, y_max, dx, dy):

        x = np.linspace(x_min, x_max, (int(abs(x_max-x_min)/dx)))
        y = np.linspace(y_min, y_max, (int(abs(y_max-y_min)/dy)))

        Xx, Yy = np.meshgrid(x, y)
        Zz = 1/((Xx+3) ** 3 + Xx*Yy+Yy**2)
        self.ax1.plot_surface(Xx, Yy, Zz, alpha=.5)
        #lim_z = max(max(Zz))

    def Disp_Opti_Func(self):
        self.Display_function(0, 0, 100, 100, 1, 1)

    def Read_data(self):
        data = pd.read_csv('test.csv')
        x = data["X"]
        y = data["Y"]
        z = data["Z"]
        X.clear()
        Y.clear()
        Z.clear()
        pom_x = []
        pom_y = []
        pom_z = []

        i = 0
        while (i < (int(self.pop.get()) * int(self.cans.get()))):
            pom_x.clear()
            pom_y.clear()
            pom_z.clear()
            for j in range(int(self.cans.get())):
                pom_x.append(x[j+i])
                pom_y.append(y[j+i])
                pom_z.append(z[j+i])
            X.append(pom_x.copy())
            Y.append(pom_y.copy())
            Z.append(pom_z.copy())
            i += int(self.cans.get())


def main():
    root = tk.Tk()
    app = App(root)
    app.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
