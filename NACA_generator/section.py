from typing import Tuple
import numpy as np
import matplotlib.pyplot as plt


class SectionNACA:
    def __init__(
            self,
            max_camber: float,
            max_camber_pos: float,
            max_thickness: float,
            num_pts: int,
            generate_closed_trailing_edge: bool = True
    ) -> None:
        self.max_camber = max_camber
        self.max_camber_pos = max_camber_pos
        self.max_thickness = max_thickness
        self.num_pts = num_pts
        self.generate_closed_trailing_edge = generate_closed_trailing_edge

        self._cosinus_spacing()

    def _thickness_distribution(self, pts: np.ndarray) -> np.ndarray:
        """
        Function calculates the thickness distribution y_t of the given NACA-airfoil.

        Parameters:
            pts: (np.array) an array with x-coordinates to evaluate the y_t
                function of the thickness distribution

        Returns:
            (np.array) an array with the thickness distribution y_t
        """
        t = self.max_thickness
        a_0 = 0.2969
        a_1 = -0.126
        a_2 = -0.3516
        a_3 = 0.2843
        a_4 = 0

        match self.generate_closed_trailing_edge:
            case True:
                a_4 = -0.1036
            case False:
                a_4 = -0.1015
            case _:
                raise ValueError(f'INPUT ERROR: generate_closed_trailing_edge must be of type bool.')

        return (5 * t) * (a_0 * np.sqrt(pts) + a_1 * pts + a_2 * pts ** 2 + a_3 * pts ** 3 + a_4 * pts ** 4)

    def _airfoil_envelope(self, pts: np.ndarray) -> np.ndarray:
        """
        Function calculates the airfoil envelope y_c of the given NACA-airfoil.

        Parameters:
            pts: (np.array) an array with x-coordinates

        Returns:
            (np.array) an array with the airfoil envelope y_c
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
                    pts: (np.array) an array with x-coordinates

                Returns:
                    (np.array) an array with the gradient of the airfoil envelope dy_c/dx
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
            pts: (np.array) an array with gradients

        Returns:
            (np.array) an array with theta for each gradient
        """
        return np.arctan(pts)

    def _cosinus_spacing(self) -> None:
        """
        Function ensures a cosinus spacing for the points with uniform increments of beta.
        """
        beta = np.linspace(0, np.pi, self.num_pts)

        self.pts = (1 - np.cos(beta)) / 2

    @property
    def suction_side(self) -> np.ndarray:
        """
        Function calculates (x, y) points for the suction side of the airfoil.
        """

        x_suc = self.pts - self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts)))
        y_suc = self._airfoil_envelope(self.pts) + self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts)))

        return np.array([x_suc, y_suc])

    @property
    def pressure_side(self) -> np.ndarray:
        """
        Function calculates (x, y) points for the pressure side of the airfoil.
        """

        x_press = self.pts + self._thickness_distribution(self.pts) * np.sin(self._theta(self._gradient(self.pts)))
        y_press = self._airfoil_envelope(self.pts) - self._thickness_distribution(self.pts) * np.cos(self._theta(self._gradient(self.pts)))

        return np.array([x_press, y_press])

class Section3D(SectionNACA):
    def __init__(
            self,
            max_camber: float,
            max_camber_pos: float,
            max_thickness: float,
            num_pts: int,
            z_pos: float,
        generate_closed_trailing_edge: bool = True
    ) -> None:
        super().__init__(max_camber, max_camber_pos, max_thickness, num_pts, generate_closed_trailing_edge)
        self.z_pos = z_pos


    @property
    def pressure_side3d(self) -> np.ndarray:

        x_pts, y_pts = self.pressure_side
        z_pts = np.full(len(x_pts), self.z_pos)

        return np.array([x_pts, y_pts, z_pts])

    @property
    def suction_side3d(self) -> np.ndarray:

        x_pts, y_pts = self.suction_side
        z_pts = np.full(len(x_pts), self.z_pos)

        return np.array([x_pts, y_pts, z_pts])


if __name__ == '__main__':

    max_camber = 0.05
    max_camber_pos = 0.4
    max_thickness = 0.12
    num_pts = 50
    airfoil = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    suction = airfoil.suction_side
    pressure = airfoil.pressure_side

    z_position = 2
    blade3d = Section3D(max_camber, max_camber_pos, max_thickness, num_pts, z_position, True)

    pressure3d = blade3d.pressure_side3d
