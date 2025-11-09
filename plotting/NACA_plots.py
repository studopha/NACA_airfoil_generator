import numpy as np
import matplotlib.pyplot as plt
from NACA_generator.NACA_airfoil import NACA4


class NACA_plots:
    def __init__(self, airfoil: NACA4):
        self.airfoil = airfoil

    def plot_2D(self):
        x_u, y_u = self.airfoil.calculate_upper_surface()
        x_l, y_l = self.airfoil.calculate_lower_surface()

        plt.plot(x_l, y_l)
        plt.plot(x_u, y_u)
        plt.title(f"{self.airfoil.profile_name}")
        plt.grid(True)
        plt.xlim(-0.1, 1.1)
        plt.ylim(-0.5, 0.5)
        plt.show()

if __name__ == '__main__':
    airfoil = NACA4('NACA6412', 100)
    test_plot = NACA_plots(airfoil)
    test_plot.plot_2D()