"""
Plot the gerated NACA blade profiles

This module provides classes for plotting NACA blades in two-dimensional
and three-dimensional representations.

:author: Ole Hartmann
:version: 1.0
:date: 2025-12-20
"""

# TODO 1. create figure
# TODO 2. Add plots
# TODO 3. 2d 3d case
# TODO 4. change plot parameters
# TODO 5. Add Title etc.
import numpy as np
import matplotlib.pyplot as plt

from blade_section.section_generator import Section2D, Section3D, extract_values_from_NACA
from blade_generator.blade_generator import BladeGenerator

class Plotter:
    """
    class to handle the plots of the sections.
    """
    def __init__(self, dimensions: int = 2):

        self.dimensions = dimensions

        match dimensions:
            case 2:
                self.fig, self.ax = plt.subplots()
            case 3:
                self.fig = plt.figure()
                self.ax = self.fig.add_subplot(projection='3d')
            case _:
                raise ValueError(f'ERROR: Invalid dimension ({dimensions}) choose 2 or 3 instead.')

    def add_2d_plot(self, section: Section2D, plot_norm_section: bool = False) -> None:

        if plot_norm_section:
            # Suction side
            self.ax.scatter(section.norm_suction_side[:, 0], section.norm_suction_side[:, 1])

            # Pressure side
            self.ax.scatter(section.norm_pressure_side[:, 0], section.norm_pressure_side[:, 1])

            # Camber line
            camber_line = section.norm_camber_line
            self.ax.plot(camber_line[:, 0], camber_line[:, 1])
        else:
            # Suction side
            self.ax.scatter(section.suction_side[:, 0], section.suction_side[:, 1])

            # Pressure side
            self.ax.scatter(section.pressure_side[:, 0], section.pressure_side[:, 1])

            # Camber line
            camber_line = section.camber_line
            self.ax.plot(camber_line[:, 0], camber_line[:, 1])

    def configure_2d_axis(self, title) -> None:
        self.ax.set_title(title)
        self.ax.grid(True)
        self.ax.axis('equal')

    def add_3d_plot(self, section: Section3D, plot_norm_sections: bool = False) -> None:
        if plot_norm_sections:
            # Suction side
            self.ax.scatter(section.norm_suction_side[:, 0], section.norm_suction_side[:, 1], section.norm_suction_side[:, 2])

            # Pressure side
            self.ax.scatter(section.norm_pressure_side[:, 0], section.norm_pressure_side[:, 1], section.norm_pressure_side[:, 2])

            # Camber line
            camber_line = section.norm_camber_line
            self.ax.plot(camber_line[:, 0], camber_line[:, 1], camber_line[:, 2])
        else:
            # Suction side
            self.ax.scatter(section.suction_side[:, 0], section.suction_side[:, 1], section.suction_side[:, 2])

            # Pressure side
            self.ax.scatter(section.pressure_side[:, 0], section.pressure_side[:, 1], section.pressure_side[:, 2])

            # Camber line
            camber_line = section.camber_line
            self.ax.plot(camber_line[:, 0], camber_line[:, 1], camber_line[:, 2])

    def configure_3d_axis(self, title) -> None:

        self.ax.set_title(title)
        self.ax.axis('equal')

    def add_blade_plot(self, blade: BladeGenerator, plot_norm_sections: bool = False) -> None:

        for i, section in enumerate(blade.sections):
            if plot_norm_sections:
                self.add_3d_plot(section, True)
            else:
                self.add_3d_plot(section, False)

    def add_blade_TE_LE(self, blade: BladeGenerator) -> None:

        leading_edge = blade.leading_edge
        trailing_edge = blade.trailing_edge

        self.ax.plot(leading_edge[:, 0], leading_edge[:, 1], leading_edge[:, 2])
        self.ax.plot(trailing_edge[:, 0], trailing_edge[:, 1], trailing_edge[:, 2])

    @staticmethod
    def show_plot(block: bool = True) -> None:
        plt.show(block=block)

if __name__ == '__main__':
    pts = 25
    length = 5
    sections = 6

    plot_blade = True
    if plot_blade:
        name_start = 'NACA9512'
        chord = 5
        max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_start)
        start_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, 0)
        start_profile.rotate_section(45, np.array([0, 0, 0]))


        name_end = 'NACA9512'
        chord = 1
        max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_end)
        end_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, length)
        end_profile.rotate_section(0, np.array([0, 0, 0]))

        blade = BladeGenerator(start_profile, end_profile, sections, pts)
        blade.scale_blade(1, 2)

        plotter = Plotter(dimensions=3)
        #plotter.add_blade_plot(blade, True)
        plotter.add_blade_plot(blade, False)
        plotter.add_blade_TE_LE(blade)
        plotter.configure_3d_axis('Test')
        plotter.show_plot()
    else:
        name_start = 'NACA9512'
        z = 2
        chord = 1
        max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_start)
        start_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, z)
        start_profile.scale_section(1)
        start_profile.rotate_section(45, np.array([0.5, 0.1, z]))

        plotter = Plotter(dimensions=3)
        plotter.add_3d_plot(start_profile, False)
        plotter.add_3d_plot(start_profile, True)

        plotter.configure_2d_axis(name_start)
        plotter.show_plot()








