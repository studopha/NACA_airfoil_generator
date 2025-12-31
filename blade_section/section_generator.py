"""
Generate NACA blade profiles

This module provides classes for generating NACA airfoil sections
in two-dimensional and three-dimensional representations.

:author: Ole Hartmann
:version: 1.0
:date: 2025-12-20
"""

# TODO symmetrical airfoils
# TODO TE LE not as property
# TODO 3d TE LE with super()
# TODO Twist
# TODO Scaling scaling applied as a fnc not on init ... self.suction_side = apply_scaling(self.suction_side)
# TODO keep unchanged norm and extra changend form


import numpy as np
from typing import Tuple

def extract_values_from_NACA(NACA_profile_name: str) -> Tuple[float, float, float]:
    """
    Function returns the values for the maximum camber, maximum camber position and the maximum thickness
    of the NACA blade from the name of the profile.

    Parameters:
        NACA_profile_name: (str) Name of the NACA profile with the format 'NACAxxxx'

    Returns:
        (Tuple[float, float, float]) Tuple of type (max_camber, max_camber_pos, max_thickness)

    Example:

        NACA_profile_name = 'NACA9512'

        max_camber = 0.09
        max_camber_pos = 0.5
        max_thickness = 0.12
    """
    max_camber = int(NACA_profile_name[4]) / 100
    max_camber_position = int(NACA_profile_name[5]) / 10
    max_thickness = int(NACA_profile_name[6:8]) / 100

    return max_camber, max_camber_position, max_thickness

class Section2D:
    """Generator class for the NACA profile section in 2D with the given values."""

    def __init__(
            self,
            max_camber: float,
            max_camber_pos: float,
            max_thickness: float,
            chord_len: float,
            num_pts: int,
    ):
        self.max_camber = max_camber
        self.max_camber_pos = max_camber_pos
        self.max_thickness = max_thickness
        self.chord_len = chord_len
        self.num_pts = num_pts
        self.suction_side = None
        self.pressure_side = None
        self.leading_edge = None
        self.trailing_edge = None

        self._check_inputs()
        self._cosine_spacing()
        self._suction_side()
        self._pressure_side()
        self._chord()
        self._leading_edge()
        self._trailing_edge()

    def _check_inputs(self) -> None:
        """
        Function validates all the inputs of the class.
        """
        inputs = [self.max_camber, self.max_camber_pos, self.max_thickness, self.num_pts]
        negative_inputs = [x for x in inputs if x < 0]
        if len(negative_inputs) > 0:
            raise ValueError(f'input argument must be positive!')
        if not isinstance(self.num_pts, int):
            raise ValueError(f'num_pts must be an integer!')

    def _thickness_distribution(self, pts: np.ndarray) -> np.ndarray:
        """
        Function calculates the thickness distribution y_t of the given NACA-blade.

        Parameters:
            pts: (np.ndarray) an array with x-coordinates to evaluate the y_t
                function of the thickness distribution

        Returns:
            (np.ndarray) an array with the thickness distribution y_t
        """
        t = self.max_thickness
        a_0 = 0.2969
        a_1 = -0.126
        a_2 = -0.3516
        a_3 = 0.2843
        a_4 = -0.1036

        return (5 * t) * (a_0 * np.sqrt(pts) + a_1 * pts + a_2 * pts ** 2 + a_3 * pts ** 3 + a_4 * pts ** 4)

    def _airfoil_envelope(self, pts: np.ndarray) -> np.ndarray:
        """
        Function calculates the airfoil envelope y_c of the given NACA-blade.

        Parameters:
            pts: (np.ndarray) an array with x-coordinates

        Returns:
            (np.ndarray) an array with the airfoil envelope y_c
        """
        m = self.max_camber
        p = self.max_camber_pos
        envelope = np.where(
            pts < p,
            (m / p ** 2) * (2 * p * pts - pts ** 2),
            (m / (1 - p) ** 2) * (1 - 2 * p + 2 * p * pts - pts ** 2)
        )

        return envelope

    def _gradient(self, pts: np.ndarray) -> np.ndarray:
        """
        Function calculates the gradient dy_c/dx of the airfoil envelope of the given NACA-airfoil.

        Parameters:
            pts: (np.ndarray) an array with x-coordinates

        Returns:
            (np.ndarray) an array with the gradient of the airfoil envelope dy_c/dx
        """
        m = self.max_camber
        p = self.max_camber_pos
        gradient = np.where(
            pts < p,
            ((2 * m) / (p ** 2)) * (p - pts),
            ((2 * m) / (1 - p) ** 2) * (p - pts)
        )

        return gradient

    @staticmethod
    def _theta(pts: np.ndarray) -> np.ndarray:
        """
        Function calculates theta.

        Parameters:
            pts: (np.ndarray) an array with gradients

        Returns:
            (np.ndarray) an array with theta for each gradient
        """
        return np.arctan(pts)

    def _cosine_spacing(self) -> None:
        """
        Function ensures a cosinus spacing for the points with uniform increments of beta.
        """
        beta = np.linspace(0, np.pi, self.num_pts)

        self.pts = (1 - np.cos(beta)) / 2

    def _suction_side(self) -> None:
        """
        Function calculates (x, y) points for the suction side of the blade.

        Returns:
            (np.ndarray) points of the suction side.
        """
        x = (self.pts -
                 self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts))))
        y = (self._airfoil_envelope(self.pts) +
                 self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts))))

        self.suction_side = np.column_stack((x, y))

    def _pressure_side(self) -> None:
        """
        Function calculates (x, y) points for the pressure side of the blade.
        """
        x = (self.pts +
                   self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts))))
        y = (self._airfoil_envelope(self.pts) -
                   self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts))))

        self.pressure_side = np.column_stack((x, y))

    def _leading_edge(self) -> None:
        """
        Function calculates the leading edge of the given 2D section and return it.

        Returns:
            (np.ndarray) the point (x, y) of the leading edge in the profile.
        """
        x = self.suction_side[0, 0]
        y = self.suction_side[0, 1]

        self.leading_edge = np.array([x, y])

    def _trailing_edge(self) -> None:
        """
        Function calculates the trailing edge of the given 2D section and return it.

        Returns:
            (np.ndarray) the point (x, y) of the trailing edge in the profile.
        """
        x = self.suction_side[-1, 0]
        y = self.suction_side[-1, 1]

        self.trailing_edge = np.array([x, y])

    def _chord(self) -> None:

        self.suction_side *= self.chord_len
        self.pressure_side *= self.chord_len


class Section3D(Section2D):
    """Generator class for the NACA profile section in 3D with the given values."""

    def __init__(
            self,
            max_camber: float,
            max_camber_pos: float,
            max_thickness: float,
            chord_len: float,
            num_pts: int,
            z_pos: float,
    ):
        self.z_pos = z_pos
        super().__init__(max_camber, max_camber_pos, max_thickness, chord_len, num_pts)


    def _pressure_side(self) -> None:
        """
        Function calculates (x, y, z) points for the pressure side of the blade.

        Returns:
            (np.ndarray) Array with the 3d points of the pressure side.
        """
        x = (self.pts +
             self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts))))
        y = (self._airfoil_envelope(self.pts) -
             self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts))))
        z = np.full(len(x), self.z_pos)

        self.pressure_side = np.column_stack((x, y, z))

    def _suction_side(self) -> None:
        """
        Function calculates (x, y, z) points for the suction side of the blade.

        Returns:
            (np.ndarray) Array with the 3d points of the suction side.
        """
        x = (self.pts -
             self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts))))
        y = (self._airfoil_envelope(self.pts) +
             self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts))))
        z = np.full(len(x), self.z_pos)

        self.suction_side = np.column_stack((x, y, z))


    def _leading_edge(self) -> None:
        """
        Function calculates the leading edge of the given 2D section and return it.

        Returns:
            (np.ndarray) the point (x, y) of the leading edge in the profile.
        """
        x = self.suction_side[0, 0]
        y = self.suction_side[0, 1]

        self.leading_edge = np.array([x, y, self.z_pos])

    def _trailing_edge(self) -> None:
        """
        Function calculates the trailing edge of the given 2D section and return it.

        Returns:
            (np.ndarray) the point (x, y) of the trailing edge in the profile.
        """
        x = self.suction_side[-1, 0]
        y = self.suction_side[-1, 1]

        self.trailing_edge = np.array([x, y, self.z_pos])

    def _chord(self) -> None:

        self.suction_side[:, :2] *= self.chord_len
        self.pressure_side[:, :2] *= self.chord_len
