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
            sections_amount: int,
            pts_per_section: int
    ):
        self.start_profile = start_profile
        self.end_profile = end_profile
        self.blade_length = self._calc_length()
        self.sections_amount = sections_amount
        self.pts_per_section = pts_per_section

        self.sections: List[section_generator.Section3D] = []
        self._create_sections()

        self.norm_leading_edge = self._create_norm_LE()
        self.norm_trailing_edge = self._create_norm_TE()


    def _calc_length(self) -> float:
        start_z = self.start_profile.z_pos
        end_z = self.end_profile.z_pos

        return end_z - start_z

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
            self.start_profile.z_pos,
            self.end_profile.z_pos,
            self.sections_amount
        )
        chord = np.linspace(
            self.start_profile.chord_len,
            self.end_profile.chord_len,
            self.sections_amount
        )
        angle = np.linspace(
            self.start_profile.angle,
            self.end_profile.angle,
            self.sections_amount
        )

        for i in range(len(max_camber)):
            self.sections.append(
                section_generator.Section3D(
                    max_camber[i],
                    max_camber_pos[i],
                    max_thickness[i],
                    chord[i],
                    self.pts_per_section,
                    z_position[i]
                )
            )

        for i, section in enumerate(self.sections):
            if angle[i] != 0:
                print('hund')
                ref = np.array([0.5, 0.1, section.z_pos])
                section.rotate_section(angle[i], ref)


    def _create_norm_LE(self) -> np.ndarray:
        """
        Function creates the curve for the leading edge of the blade geometry.

        Returns:
            (np.ndarray) Pointcloud (x, y, z) of the leading edge of the blade geometry.
        """
        leading_edge = []
        for section in self.sections:
            leading_edge.append(section.norm_leading_edge)

        return np.array(leading_edge)

    def _create_norm_TE(self) -> np.ndarray:
        """
        Function creates the curve for the trailing edge of the blade geometry.

        Returns:
            (np.ndarray) Pointcloud (x, y, z) of the trailing edge of the blade geometry.
        """
        trailing_edge = []
        for section in self.sections:
            trailing_edge.append(section.norm_trailing_edge)

        return np.array(trailing_edge)

    @property
    def leading_edge(self) -> np.ndarray:
        leading_edge = []
        for section in self.sections:
            leading_edge.append(section.leading_edge)

        return np.array(leading_edge)

    @property
    def trailing_edge(self) -> np.ndarray:
        trailing_edge = []
        for section in self.sections:
            trailing_edge.append(section.trailing_edge)

        return np.array(trailing_edge)

    def scale_blade(self, start_factor: float, end_factor: float) -> None:

        factor = np.linspace(
            start_factor,
            end_factor,
            self.sections_amount
        )

        for i, section in enumerate(self.sections):
            section.scale_section(factor[i])