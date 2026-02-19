import numpy as np

from blade_generator.blade_generator import BladeGenerator
from blade_section.section_generator import Section2D, Section3D, extract_values_from_NACA



def export_to_csv(name: str, blade: BladeGenerator) -> None:



    for i, section in enumerate(blade.sections):
        pts = np.vstack((section.pressure_side[:-1], section.suction_side[::-1]))
        #pts = pts[:-1]
        np.savetxt(f'{name}{i}.csv', pts, delimiter=';')

def export_to_txt(name:str, blade: BladeGenerator) -> None:

    for i, section in enumerate(blade.sections):
        pts = np.vstack((section.pressure_side[:-1], section.suction_side[::-1]))
        #pts = pts[:-1]
        np.savetxt(
            f'{name}{i}.txt',
            pts,
            #header='Polyline=False\n3D=True',
            comments='',
            delimiter='\t',
        )





if __name__ == '__main__':
    pts = 100
    length = 10
    sections = 6
    ref = np.array([0.5, 0.1])  # implement it not hardcode

    name_start = 'NACA9412'
    chord = 5
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_start)
    max_camb = 0.2
    start_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, 0)

    name_end = 'NACA9512'
    chord = 1
    max_camb, max_camb_pos, max_thic = extract_values_from_NACA(name_end)
    end_profile = Section3D(max_camb, max_camb_pos, max_thic, chord, pts, length)

    blade = BladeGenerator(start_profile, end_profile, sections, pts)
    blade.scale_blade(3, 1)
    blade.rotate_blade(0, 45, ref)
    blade.alignment(method='center')

    path = r'X:\Python\NACA_airfoil_generator\export\test'
    export_to_txt(path, blade)



