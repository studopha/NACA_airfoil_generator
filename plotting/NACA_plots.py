import numpy as np
import matplotlib.pyplot as plt

from NACA_generator.NACA_airfoil import NACA4
from NACA_generator.section import SectionNACA, Section3D
from typing import List

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
        plt.ioff()
        plt.show()

def plot_section(profile: SectionNACA, name: str = ''):
    fig = plt.figure()

    # Suction side
    plt.plot(profile.suction_side[0], profile.suction_side[1])

    # Pressure side
    plt.plot(profile.pressure_side[0], profile.pressure_side[1])

    plt.title(name)
    plt.grid(True)
    plt.xlim( -0.1, 1.1)
    plt.ylim(-0.5, 0.5)
    plt.axis('equal')
    plt.show(block=False)

def plot_3d(profiles: List[Section3D], name: str = '') -> None:

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')

    for profile in profiles:
        # Suction side
        x_suc, y_suc, z_suc = profile.suction_side3d
        ax.scatter(x_suc, y_suc, z_suc)

        # Pressure side
        x_pres, y_pres, z_pres = profile.pressure_side3d
        ax.scatter(x_pres, y_pres, z_pres)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.title(name)
    plt.axis('equal')
    plt.show()



if __name__ == '__main__':
    max_camber = 0.05
    max_camber_pos = 0.4
    max_thickness = 0.12
    num_pts = 50
    airfoil = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    plot_section(airfoil)