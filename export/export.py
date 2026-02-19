"""Handler for the export of the generated blades"""

import numpy as np

from NACA_generator.blade_3d import Blade3D
from NACA_generator.section import Section3D


class Exporter:
    def __init__(self):
        pass

    def export_section(self, file_name: str, section: Section3D) -> None:
        pts_suc = section.suction_side3d
        pts_pres = section.pressure_side3d

        all_pts = np.hstack((pts_suc, pts_pres[::-1]))

        np.savetxt(
            fr'{file_name}',
            all_pts.T,
            delimiter=';',
        )