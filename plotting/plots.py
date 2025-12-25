"""
Plot the gerated NACA blade profiles

This module provides classes for plotting NACA blades in two-dimensional
and three-dimensional representations.

:author: Ole Hartmann
:version: 1.0
:date: 2025-12-20
"""

import numpy as np
import matplotlib.pyplot as plt

from blade_section.section_generator import Section2D, Section3D, extract_values_from_NACA
from blade_generator.blade_generator import BladeGenerator

class Plotter:
    """
    class to handle the plots of the sections.
    """

    def plot2D(self, section: Section2D, title: str = 'NACA blade') -> None:
        """
        Function plots a two-dimensional section as a point cloud.

        :param section:
        :return:
        """
        lim_dif = 0.1
        x_min = min(np.min(section.suction_side[:, 0]), np.min(section.pressure_side[:, 0]))
        x_max = max(np.max(section.suction_side[:, 0]), np.max(section.pressure_side[:, 0]))
        x_span = abs(x_max) - abs(x_min)
        x_lim = (x_min - x_span * lim_dif, x_max + x_span * lim_dif)

        y_min = min(np.min(section.suction_side[:, 1]), np.min(section.pressure_side[:, 1]))
        y_max = max(np.max(section.suction_side[:, 1]), np.max(section.pressure_side[:, 1]))
        y_span = abs(y_max) - abs(y_min)
        y_lim = (y_min - y_span * lim_dif, y_max + y_span * lim_dif)

        fig = plt.figure()

        # Suction side
        plt.scatter(section.suction_side[:, 0], section.suction_side[:, 1])

        # Pressure Side
        plt.scatter(section.pressure_side[:, 0], section.pressure_side[:, 1])

        plt.title(title)
        plt.grid(True)
        #plt.xlim(x_lim)
        #plt.ylim(y_lim)
        plt.axis('equal')
        plt.show()

    def plot3D(self, section: Section3D) -> None:
        """
        Function plots a three-dimnesional section as a points cloud.
        """
        pass

    def plot_blade(self, blade: BladeGenerator) -> None:


        pass

if __name__ == '__main__':
    name = 'NACA9512'
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name)
    profile = Section2D(max_camb, max_camb_pos, max_thic, 20)

    plotter = Plotter()

    plotter.plot2D(profile)

