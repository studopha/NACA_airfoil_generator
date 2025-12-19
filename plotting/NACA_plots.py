import numpy as np
import matplotlib.pyplot as plt

from NACA_generator.NACA_airfoil import NACA4
from NACA_generator.section import SectionNACA, Section3D
from NACA_generator.blade_3d import Blade3D, extract_from_name
from export.export import Exporter
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
    #plt.plot(profile.suction_side[0], profile.suction_side[1])
    plt.scatter(profile.suction_side[0], profile.suction_side[1])

    # Pressure side
    #plt.plot(profile.pressure_side[0], profile.pressure_side[1])
    plt.scatter(profile.pressure_side[0], profile.pressure_side[1])

    plt.title(name)
    plt.grid(True)
    plt.xlim( -0.1, 1.1)
    plt.ylim(-0.5, 0.5)
    plt.axis('equal')
    plt.show(block=False)

def plot_3d(blade: Blade3D, name: str = '', edges: bool = True) -> None:

    fig = plt.figure()
    ax = fig.add_subplot(projection='3d')


    for i, profile in enumerate(blade.sections):
        # Suction side
        x_suc, y_suc, z_suc = profile.suction_side3d
        ax.scatter(x_suc, y_suc, z_suc)

        # Pressure side
        x_pres, y_pres, z_pres = profile.pressure_side3d
        ax.scatter(x_pres, y_pres, z_pres)

        # Text display
        text_disp = True
        if text_disp:
            text = f'Sektion {i + 1}'
            x_txt, y_txt, z_txt = profile.trailing_edge

            print(x_txt)

            ax.text(
                x_txt + 0.2 , y_txt + 0.1, z_txt,
                text,
                fontsize=10,
                color='black'
            )


    if edges:
        x_LE, y_LE, z_LE = blade.leading_edge
        x_TE, y_TE, z_TE = blade.trailing_edge


        print(blade.leading_edge)
        print(blade.trailing_edge)
        plt.plot(x_LE, y_LE, z_LE)
        plt.plot(x_TE, y_LE, z_TE)

    ax.set_xlabel('x')
    ax.set_ylabel('y')
    ax.set_zlabel('z')

    plt.grid(False)
    plt.title(name)
    plt.axis('equal')
    plt.show()
    plt.ion()


if __name__ == '__main__':

    num_pts = 50
    # Start profile
    profile_name = 'NACA9525'
    max_camber, max_camber_pos, max_thickness = extract_from_name(profile_name)
    profile_start = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    # End profile
    profile_name = 'NACA9510'
    max_camber, max_camber_pos, max_thickness = extract_from_name(profile_name)
    profile_end = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    sections = 6

    length = 3
    profile_3d = Blade3D(profile_start, profile_end, length, sections, num_pts)

    for i, section in enumerate(profile_3d.sections):
        name = f'NACA 9525'
        #plot_section(section, name)

    #plot_3d(profile_3d, 'NACA Profil')

    exporter = Exporter()

    exporter.export_section(r'X:\Python\NACA_airfoil_generator\NACA_generator\3d_profile.csv', profile_3d.sections[0])