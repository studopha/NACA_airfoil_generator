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

    def add_2d_plot(self, section: Section2D) -> None:
        # Suction side
        self.ax.scatter(section.suction_side[:, 0], section.suction_side[:, 1])

        # Pressure side
        self.ax.scatter(section.pressure_side[:, 0], section.pressure_side[:, 1])

    def configure_2d_axis(self, title) -> None:
        self.ax.set_title(title)
        self.ax.grid(True)
        self.ax.axis('equal')

    def add_3d_plot(self, section: Section3D) -> None:
        # Suction side
        self.ax.scatter(section.suction_side[:, 0], section.suction_side[:, 1], section.suction_side[:, 2])

        # Pressure side
        self.ax.scatter(section.pressure_side[:, 0], section.pressure_side[:, 1], section.pressure_side[:, 2])

    def configure_3d_axis(self, title) -> None:

        self.ax.set_title(title)
        self.ax.axis('equal')

    def add_blade_plot(self, blade: BladeGenerator) -> None:

        for i, section in enumerate(blade.sections):
            self.add_3d_plot(section)

    @staticmethod
    def show_plot(block: bool = True) -> None:
        plt.show(block=block)

if __name__ == '__main__':
    pts = 25
    length = 20
    sections = 6


    name_start = 'NACA9420'
    chord = 5
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_start)
    start_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, 0)

    name_end = 'NACA9512'
    chord = 1
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_end)
    end_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, length)

    blade = BladeGenerator(start_profile, end_profile, sections, pts)


    plotter = Plotter(dimensions=3)
    plotter.add_blade_plot(blade)
    plotter.configure_3d_axis('Test')
    plotter.show_plot()



    name_start = 'NACA9420'
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_start)
    start_profile = Section2D(max_camb, max_camb_pos, max_thic, chord, pts)


    plotter = Plotter(dimensions=2)
    plotter.add_2d_plot(start_profile)
    plotter.configure_2d_axis(name_start)
    plotter.show_plot()




