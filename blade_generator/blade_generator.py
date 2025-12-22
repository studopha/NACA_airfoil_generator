"""
Generate NACA blade profiles

This module provides classes for generating NACA airfoil sections
in two-dimensional and three-dimensional representations.

:author: Ole Hartmann
:version: 1.0
:date: 2025-12-20
"""

import numpy as np
from typing import List

import blade_section.section_generator as section_generator


class BladeGenerator:
    def __init__(
            self,
            start_profile: section_generator.Section3D,
            end_profile: section_generator.Section3D,
            blade_length: float,
            sections_amount: int,
            pts_per_section: int
    ):
        self.start_profile = start_profile
        self.end_profile = end_profile
        self.blade_length = blade_length
        self.sections_amount = sections_amount
        self.pts_per_section = pts_per_section

        self.sections: List[section_generator.Section3D] = []
        self._create_sections()

        self.leading_edge = self._create_LE()
        self.trailing_edge = self._create_TE()

    def _create_sections(self) -> None:
        """
        Function creates the three-dimensional sections that lie between the starting and the ending section.
        """
        max_camber = np.linspace(
            self.start_profile.max_camber,
            self.end_profile.max_camber,
            self.sections_amount
        )
        max_camber_pos = np.linspace(
            self.start_profile.max_camber_pos,
            self.end_profile.max_camber_pos,
            self.sections_amount
        )
        max_thickness = np.linspace(
            self.start_profile.max_thickness,
            self.end_profile.max_thickness,
            self.sections_amount
        )
        z_position = np.linspace(
            0,
            self.blade_length,
            self.sections_amount
        )

        for i in range(len(max_camber)):
            self.sections.append(
                section_generator.Section3D(
                    max_camber[i],
                    max_camber_pos[i],
                    max_thickness[i],
                    self.pts_per_section,
                    z_position[i]
                )
            )

    def _create_LE(self) -> np.ndarray:
        """
        Function creates the curve for the leading edge of the blade geometry.

        Returns:
            (np.ndarray) Pointcloud (x, y, z) of the leading edge of the blade geometry.
        """
        leading_edge = []
        for section in self.sections:
            leading_edge.append(section.leading_edge)

        return np.array(leading_edge)

    def _create_TE(self) -> np.ndarray:
        """
        Function creates the curve for the trailing edge of the blade geometry.

        Returns:
            (np.ndarray) Pointcloud (x, y, z) of the trailing edge of the blade geometry.
        """
        trailing_edge = []
        for section in self.sections:
            trailing_edge.append(section.trailing_edge)

        return np.array(trailing_edge)

if __name__ == '__main__':

    num_pts = 50
    # Start profile
    profile_name = 'NACA1112'
    max_camber, max_camber_pos, max_thickness = section_generator.extract_values_from_NACA(profile_name)
    profile_start = section_generator.Section3D(max_camber, max_camber_pos, max_thickness, num_pts, True)

    # End profile
    profile_name = 'NACA9512'
    max_camber, max_camber_pos, max_thickness = section_generator.extract_values_from_NACA(profile_name)
    profile_end = section_generator.Section3D(max_camber, max_camber_pos, max_thickness, num_pts, True)

    sections = 6

    length = 2
    profile_3d = BladeGenerator(profile_start, profile_end, length, sections, num_pts)


    print(profile_3d.leading_edge)
    print(profile_3d.trailing_edge)

    print(profile_3d.leading_edge.shape)
    print(profile_3d.trailing_edge.shape)


