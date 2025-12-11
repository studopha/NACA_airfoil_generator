import numpy as np
from NACA_generator.section import SectionNACA
from plotting.NACA_plots import plot_section
from typing import List, Tuple



def extract_from_name(profile_name: str) -> Tuple[float, float, float]:
    max_camber = int(profile_name[4]) / 100
    max_camber_position = int(profile_name[5]) / 10
    max_thickness = int(profile_name[6:8]) / 100

    return max_camber, max_camber_position, max_thickness

class Blade3D:
    def __init__(
            self,
            start_profile: SectionNACA,
            end_profile: SectionNACA,
            sections_amount: int,
            pts_per_section: int
    ) -> None:

        self.start_profile = start_profile
        self.end_profile = end_profile
        self.sections_amount = sections_amount
        self.pts_per_section = pts_per_section

        self.sections = None
        self._create_sections()

    def _create_sections(self) -> None:
        max_camber = np.linspace(
            self.start_profile.max_camber,
            self.end_profile.max_camber,
            self.sections_amount - 2
        )
        max_camber_pos = np.linspace(
            self.start_profile.max_camber_pos,
            self.end_profile.max_camber_pos,
            self.sections_amount - 2
        )
        max_thickness = np.linspace(
            self.start_profile.max_thickness,
            self.end_profile.max_thickness,
            self.sections_amount - 2
        )

        sections_list = [self.start_profile]

        for i in range(len(max_camber)):  # -1 to remove start and end section
            sections_list.append(SectionNACA(max_camber[i], max_camber_pos[i], max_thickness[i], self.pts_per_section, True))

        sections_list.append(self.end_profile)

        self.sections = sections_list



if __name__ == '__main__':

    num_pts = 50
    # Start profile
    profile_name = 'NACA1112'
    max_camber, max_camber_pos, max_thickness = extract_from_name(profile_name)
    profile_start = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    # End profile
    profile_name = 'NACA9512'
    max_camber, max_camber_pos, max_thickness = extract_from_name(profile_name)
    profile_end = SectionNACA(max_camber, max_camber_pos, max_thickness, num_pts, True)

    sections = 6

    profile_3d = Blade3D(profile_start, profile_end, sections, num_pts)


    for i, section in enumerate(profile_3d.sections):
        name = f'section {i}'
        plot_section(section, name)


    #plot_section(profile_start)
    #plot_section(profile_end)
