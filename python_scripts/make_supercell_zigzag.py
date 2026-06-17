from ase.io import read, write
from ase.build import make_supercell
import numpy as np

# ---------------- USER INPUT ----------------
input_file = input("Input POSCAR filename [POSCAR original]: ").strip()

nx = int(input("Expansion coefficient nx: "))
ny = int(input("Expansion coefficient ny: "))
nz = int(input("Expansion coefficient nz: "))

# store scaling for nanotube step
with open("scale.txt", "w") as f:
    f.write(f"{nx}\n{ny}\n{nz}\n")

print(f"\nReading structure: {input_file}")

atoms = read(input_file)

P = np.array([
    [nx, 0,  0],
    [0,  ny, 0],
    [0,  0,  nz]
])

supercell = make_supercell(atoms, P)

write("POSCAR_supercell", supercell, format="vasp", direct=True, sort=True)

print("\n========== SUMMARY ==========")
print("Atoms (primitive):", len(atoms))
print("Atoms (supercell):", len(supercell))
print("=============================")
