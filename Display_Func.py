import random
import numpy as np
import matplotlib.pyplot as plot
from matplotlib.animation import FuncAnimation
import csv
import pandas as pd

X, Y, Z = [], [], []
ax = plot.axes(projection="3d")


def Read_data():
    data = pd.read_csv('test.csv')
    x = data["X"]
    y = data["Y"]
    z = data["Z"]
    pom_x = []
    pom_y = []
    pom_z = []

    i = 0
    while (i < 190):
        pom_x.clear()
        pom_y.clear()
        pom_z.clear()
        for j in range(10):
            pom_x.append(x[j+i])
            pom_y.append(y[j+i])
            pom_z.append(z[j+i])
        X.append(pom_x.copy())
        Y.append(pom_y.copy())
        Z.append(pom_z.copy())
        i += 10

# Funkcja Optymalizowana


def Display_function(x_min, y_min, x_max, y_max, dx, dy):

    x = np.linspace(x_min, x_max, (int(abs(x_max-x_min)/dx)))
    y = np.linspace(y_min, y_max, (int(abs(y_max-y_min)/dy)))

    X, Y = np.meshgrid(x, y)
    Z = 1/((X+3) ** 3 + X*Y+Y**2)
    ax.plot_surface(X, Y, Z, alpha=.5)


def Disp_Opti_Func():
    Display_function(0, 0, 100, 100, 1, 1)


def animate(i):
    if(i < 10):
        #plot.plot(X[i], Y[i], Z[i], marker='o')
        ax.scatter3D(X[i], Y[i], Z[i], marker='o')
        i += 10


def main_func():
    Read_data()
    Disp_Opti_Func()
    ani = FuncAnimation(plot.gcf(), animate, interval=1000, repeat=False)
    plot.show()
