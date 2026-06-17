import numpy as np
from ase.io import read, write

# ----------------------------
# Load structure (supercell OK)
# ----------------------------
atoms = read("POSCAR_supercell")
cell = atoms.cell.array
positions = atoms.get_positions()

# ----------------------------
# Read scaling (for info only)
# ----------------------------
with open("scale.txt") as f:
    nx, ny, nz = [int(x) for x in f.readlines()]

print("Scaling:", nx, ny, nz)

# ----------------------------
# USER INPUT: nanotube indices
# ----------------------------
n = int(input("n (along a): "))
m = int(input("m (along b): "))

k = int(input("k (+1 or -1): "))

# ----------------------------
# reconstruct primitive lattice
# ----------------------------
a = cell[0] / nx
b = cell[1] / ny
c = cell[2] / nz

# ----------------------------
# CHIRAL VECTOR (THIS DEFINES THE TUBE)
# ----------------------------
C = n * a + m * b
C_len = np.linalg.norm(C)
C_hat = C / C_len

# tube axis (in-plane perpendicular direction)
T = np.cross(C, c)
T = T / np.linalg.norm(T)

# radius
R = C_len / (2 * np.pi)

print("Radius:", R)

# ----------------------------
# build cylindrical coordinates
# ----------------------------
new_positions = []

for r in positions:
    x0, y0, z0 = r

    r_vec = np.array([x0, y0, z0])

    # projection onto circumference direction
    x_proj = np.dot(r_vec, C_hat)

    # FULL correct angle mapping (FIXES HALF CYLINDER)
    theta = 2 * np.pi * (x_proj / C_len)

    # radius modulation (your k-term preserved)
    radius = R + ((1 - k) / 2.0) * np.linalg.norm(c) + k * z0

    # cylindrical embedding
    x1 = radius * np.cos(theta)
    y1 = radius * np.sin(theta)
    z1 = np.dot(r_vec, T)

    new_positions.append([x1, y1, z1])

# ----------------------------
# write nanotube
# ----------------------------
atoms.set_positions(np.array(new_positions))

write("POSCAR_nanostructure", atoms, format="vasp", direct=False)

print("\nDONE → POSCAR_nanostructure written")
print("Atoms:", len(atoms))
