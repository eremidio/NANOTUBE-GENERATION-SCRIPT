#!/usr/bin/env python3

from ase.io import read, write
import sys

if len(sys.argv) != 3:
    print(f"Usage: {sys.argv[0]} POSCAR_or_CONTCAR output.cif")
    sys.exit(1)

input_file = sys.argv[1]
output_file = sys.argv[2]

atoms = read(input_file, format="vasp")

write(output_file, atoms, format="cif")

print(f"Converted {input_file} -> {output_file}")

#USE THIS WITH THE COMMAND: python poscar_to_cif.py CONTCAR structure.cif
