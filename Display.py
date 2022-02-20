# Jakub Nowak 2021
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
import GA


# DISPLAY
root = tk.Tk()
best = 0
t = f'Best Result {best}'
q = tk.Label(root, text=t)
ax = plt.axes(projection="3d")
X, Y, Z = [], [], []
lim_z = 0


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

        lbl = tk.Label(btns, text="Function type")
        lbl.pack(side=tk.LEFT)

        self.pck = tk.Entry(btns, width=5)
        self.pck.insert(0, 0)
        self.pck.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Number of populations")
        lbl.pack(side=tk.LEFT)

        self.pop = tk.Entry(btns, width=5)
        self.pop.insert(0, '35')
        self.pop.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Number of candidates")
        lbl.pack(side=tk.LEFT)

        self.cans = tk.Entry(btns, width=5)
        self.cans.insert(0, '35')
        self.cans.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Initial Step")
        lbl.pack(side=tk.LEFT)

        self.step = tk.Entry(btns, width=5)
        self.step.insert(0, '6.5')
        self.step.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="P1")
        lbl.pack(side=tk.LEFT)

        self.p1 = tk.Entry(btns, width=5)
        self.p1.insert(0, '2.5')
        self.p1.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="P2")
        lbl.pack(side=tk.LEFT)

        self.p2 = tk.Entry(btns, width=5)
        self.p2.insert(0, '10')
        self.p2.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="N for best successtion")
        lbl.pack(side=tk.LEFT)

        self.n = tk.Entry(btns, width=5)
        self.n.insert(0, '10')
        self.n.pack(side=tk.LEFT)

        lbl = tk.Label(btns, text="Display type")
        lbl.pack(side=tk.LEFT)

        self.disp = tk.Entry(btns, width=5)
        self.disp.insert(0, '0')
        self.disp.pack(side=tk.LEFT)

        self.btn = tk.Button(btns, text='Start', command=self.on_click)
        self.btn.pack(side=tk.LEFT)

        B = tk.Button(btns, text="Quit", command=quit)
        B.pack(side=tk.RIGHT)

        #self.l = tk.Label(btns, text=t)
        #self.l.config(font=("Courier", 14))
        # self.l.pack(side=tk.BOTTOM)

        self.fig = plt.Figure()

        self.ax1 = self.fig.add_subplot(111, projection='3d')
        self.line, = self.ax1.plot([], [], [], marker='o')

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)

        self.canvas.get_tk_widget().pack()

    def on_click(self):
        self.ax1.cla()
        if self.ani is None:
            return self.start()

        if self.running:
            self.ani.event_source.stop()
            self.btn.config(text='Un-Pause')
        else:
            self.ani.event_source.start()
            self.btn.config(text='Pause')
        self.running = not self.running

    def start(self):
        X, Y, Z = [], [], []
        # Run algorithm
        best = GA.main(int(self.cans.get()), int(self.pop.get()),
                       int(self.pck.get()), float(self.step.get()), float(self.p1.get()), float(self.p2.get()), int(self.n.get()))
        t = f'Best Result {best}'
        q.config(text=t)
        # Read Data
        self.Read_data()
        self.ax1.cla()
        if(int(self.pck.get()) == 0 or int(self.pck.get()) == 3):
            self.ax1.set_ylim(-10, 10)
            self.ax1.set_xlim(-10, 10)
        elif(int(self.pck.get()) == 1 or int(self.pck.get()) == 2):
            self.ax1.set_ylim(-5, 5)
            self.ax1.set_xlim(-5, 5)
        self.Disp_Opti_Func()
        self.points = int(self.pop.get()) + 1
        self.ani = animation.FuncAnimation(
            self.fig,
            self.update_graph,
            frames=self.points,
            interval=int(20),
            repeat=False)
        self.running = True
        self.btn.config(text='Pause')
        self.ani._start()
        print('started animation')

    def update_graph(self, i):
        if(i < int(self.pop.get())):
            if(int(self.disp.get())):
                self.ax1.cla()
                self.Disp_Opti_Func()
                self.ax1.scatter3D(
                    X[i], Y[i], Z[i], marker='o', c='#ff7f0e')
            else:
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
        if(int(self.pck.get()) == 0):
            Zz = (Xx**2 + Yy**2)
        elif(int(self.pck.get()) == 1):
            Zz = -20.0 * np.exp(-0.2 * np.sqrt(0.5 * (Xx**2 + Yy**2))) - np.exp(
                0.5 * (np.cos(2 * np.pi * Xx) + np.cos(2 * np.pi * Yy))) + np.e + 20
        elif(int(self.pck.get()) == 2):
            Zz = (Xx**2 + Yy - 11)**2 + (Xx + Yy**2 - 7)**2
        elif(int(self.pck.get()) == 3):
            Zz = -np.absolute(np.sin(Xx) * np.cos(Yy) *
                              np.exp(np.absolute(1 - (np.sqrt(Xx**2 + Yy**2)/np.pi))))
        self.ax1.plot_surface(Xx, Yy, Zz, alpha=.5)

    def Disp_Opti_Func(self):
        if(int(self.pck.get()) == 0 or int(self.pck.get()) == 3):
            self.Display_function(-10, -10, 10, 10, 0.01, 0.01)
        elif(int(self.pck.get()) == 1 or int(self.pck.get()) == 2):
            self.Display_function(-5, -5, 5, 5, 0.01, 0.01)

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
                # print(x[j+i])
            X.append(pom_x.copy())
            Y.append(pom_y.copy())
            Z.append(pom_z.copy())
            i += int(self.cans.get())


def main():

    root.geometry("1444x900")
    Text = '''Function 0 - Unimodal Function: x\u00b2 + y\u00b2\nGlobal Optimum 0 at {0,0}
    \n\nFunction 1 - Multimodal Function: Ackley function\nGlobal Optimum 0 at {0,0}
    \n\nFunction 2 - Multimodal Function: Himmelblau's function\nLocal Minima 0 at {3,2}, {-2.8,3.13}, {-3.77,-3.28}, {3.58,-1.84}
    \n\nFunction 3 - Multimodal Function: Hölder table function\nLocal Minima -19.21 at {8,9.6}, {-8,9.6}, {8,-9.6}, {-8,-9.6}\n\n'''
    # Create label

    q.config(font=("Courier bold", 14))
    q.pack(side=tk.BOTTOM)

    l = tk.Label(root, text=Text)
    l.config(font=("Courier", 14))
    l.pack(side=tk.BOTTOM)
    root.title('Population Visualization for Genetic Algorithms')

    cr = tk.Label(root, text="©Jakub Nowak 2021")
    cr.config(font=("Calibri", 14))
    cr.pack(side=tk.TOP)

    app = App(root)
    app.pack()
    root.mainloop()


if __name__ == '__main__':
    main()
