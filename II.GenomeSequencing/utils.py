from typing import List


with open('data/integer_mass_table.txt', 'r') as reference_file:
    masses = [line.strip().split(' ') for line in reference_file.readlines()]
INTEGER_MASSES = {mass[0]: int(mass[1]) for mass in masses}
    
    
def parse_spectrum(spectrum: str) -> List[int]:
    return list(map(int, spectrum.split(' ')))


def display_spectrum(peptide: str) -> str:
    return '-'.join([str(INTEGER_MASSES[aa]) for aa in peptide])