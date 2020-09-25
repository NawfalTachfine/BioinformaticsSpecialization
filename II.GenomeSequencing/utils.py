from typing import List, Dict


with open('data/integer_mass_table.txt', 'r') as reference_file:
    masses = [line.strip().split(' ') for line in reference_file.readlines()]
INTEGER_MASSES = {mass[0]: int(mass[1]) for mass in masses}
    
    
def parse_spectrum(spectrum: str) -> List[int]:
    return list(map(int, spectrum.split(' ')))


def display_spectrum(peptide: str, integer_masses: Dict[str, int] = INTEGER_MASSES) -> str:
    return '-'.join([str(integer_masses[aa]) for aa in peptide])