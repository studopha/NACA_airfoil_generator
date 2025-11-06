import numpy as np
import matplotlib.pyplot as plt

class NACA4:
    def __init__(self, profile_name: str, num_of_pts: int, generate_closed_trailing_edge: bool = False):
        self.profile_name = profile_name
        self.num_of_pts = num_of_pts
        self.generate_closed_trailing_edge = generate_closed_trailing_edge
        self.max_camber = None
        self.max_camber_position = None
        self.max_thickness = None
        self.pts = None

        self._validate_inputs()
        self._convert_pts()

    def _validate_inputs(self) -> None:  # TODO add the input check
        self.max_camber =  int(self.profile_name[4]) / 100
        self.max_camber_position = int(self.profile_name[5]) / 10
        self.max_thickness = int(self.profile_name[6:8]) / 100

    def _thickness_distribution(self, pts: np.array) -> np.array:
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

        match self.generate_closed_trailing_edge:
            case True:
                a_4 = -0.1036
            case False:
                a_4 = -0.1015
            case _:
                raise ValueError(f'INPUT ERROR: generate_closed_trailing_edge must be of type bool.')

        return (5 * t)*(a_0 * np.sqrt(pts) + a_1 * pts + a_2 * pts**2 + a_3 * pts**3 + a_4 * pts**4)

    def _airfoil_envelope(self, pts: np.array) -> np.array:
        """
        Function calculates the airfoil envelope y_c of the given NACA-airfoil.

        Parameters:
            pts: (np.array) an array with x-coordinates

        Returns:
            (np.array) an array with the airfoil envelope y_c
        """
        m = self.max_camber
        p = self.max_camber_position
        envelope = np.zeros(self.num_of_pts)

        for i, point in enumerate(pts):
            if point < p:
                envelope[i] = (m / p**2) * (2 * p * point - point**2)
            else:
                envelope[i] = (m / (1 - p)**2) * (1 - 2 * p + 2 * p * point - point**2)

        return envelope

    def _gradient(self, pts: np.array) -> np.array:
        """
        Function calculates the gradient dy_c/dx of the airfoil envelope of the given NACA-airfoil.

        Parameters:
            pts: (np.array) an array with x-coordinates

        Returns:
            (np.array) an array with the gradient of the airfoil envelope dy_c/dx
        """
        m = self.max_camber
        p = self.max_camber_position
        gradient = np.zeros(self.num_of_pts)

        for i, point in enumerate(pts):
            if point < p:
                gradient[i] = ((2 * m) / (p**2)) * (p - point)
            else:
                gradient[i] = ((2 * m) / (1 - p)**2) * (p - point)

    @staticmethod
    def _theta(pts: np.array) -> np.array:
        """
        Function calculates theta.

        Parameters:
            pts: (np.array) an array with gradients

        Returns:
            (np.array) an array with theta for each gradient
        """
        return np.arctan(pts)

    def _convert_pts(self):
        """
        Function ensures a cosinus spacing for the points with uniform increments of beta.
        """
        beta = np.linspace(0, np.pi, self.num_of_pts)

        self.pts = (1 - np.cos(beta)) / 2

    def calculate_upper_surface(self) -> np.array:
        """
        Function calculates (x, y) points for the suction side of the airfoil.
        """

        x_u = self.pts - self._thickness_distribution(self.pts) * np.sin(self._theta(self.pts))
        y_u = self._airfoil_envelope(self.pts) + self._thickness_distribution(self.pts) * np.cos(self._theta(self.pts))

        return x_u, y_u

    def calculate_lower_surface(self) -> np.array:
        """
        Function calculates (x, y) points for the pressure side of the airfoil.
        """

        x_l = self.pts + self._thickness_distribution(self.pts) * np.sin(self._theta(self.pts))
        y_l = self._airfoil_envelope(self.pts) - self._thickness_distribution(self.pts) * np.cos(self._theta(self.pts))

        return x_l, y_l

if __name__ == '__main__':
    name = 'NACA6412'

    airfoil = NACA4(name, 100)

    x_u, y_u = airfoil.calculate_upper_surface()
    x_l, y_l = airfoil.calculate_lower_surface()

    plt.plot(x_l, y_l)
    plt.plot(x_u, y_u)
    plt.xlabel("x")
    plt.ylabel("f(x)")
    plt.title(f"{name}")
    plt.grid(True)
    plt.axis('equal')

    plt.show()