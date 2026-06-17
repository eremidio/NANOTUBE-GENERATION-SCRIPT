from ase.io import read, write
from ase.build import make_supercell
import numpy as np

# ---------------- USER INPUT ----------------
input_file = input("Input POSCAR filename [POSCAR original]: ").strip()
output_file =  "POSCAR_supercell"

nx = int(input("Expansion coefficient nx: "))
ny = int(input("Expansion coefficient ny: "))
nz = int(input("Expansion coefficient nz: "))

with open("scale.txt", "w") as n_file:
    n_file.write(f"{nx}\n")
    n_file.write(f"{ny}\n")
    n_file.write(f"{nz}\n")
# -------------------------------------------

print(f"\nReading structure: {input_file}")

# Read the original POSCAR
atoms = read(input_file)

# Transformation matrix
P = np.array([
    [nx, 0,  0],
    [0,  ny, 0],
    [0,  0,  nz]
])

# Build supercell
supercell = make_supercell(atoms, P)

# Write new POSCAR (ASE handles formatting)
write(
    "POSCAR_supercell",
    supercell,
    format="vasp",
    direct=True,
    sort=True
)

print("\n========== SUMMARY ==========")
print(f"Input file      : {input_file}")
print(f"Output file     : {output_file}")
print(f"Original atoms  : {len(atoms)}")
print(f"Supercell atoms : {len(supercell)}")
print("\nNew lattice vectors:")
print(supercell.cell)
print("=============================")
