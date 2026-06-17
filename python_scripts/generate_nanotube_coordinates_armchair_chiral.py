import numpy as np
from ase.io import read, write

# ----------------------------
# Load structure
# ----------------------------
poscar_file = "POSCAR_supercell"

atoms = read(poscar_file)

# Convert to Cartesian (IMPORTANT)
atoms = atoms.copy()
atoms.set_positions(atoms.get_positions())

cell = atoms.cell.array
positions = atoms.get_positions()

# ----------------------------
# Read scaling info
# ----------------------------
with open("scale.txt", "r") as f:
    scales = [int(line.strip()) for line in f.readlines()]

if len(scales) != 3:
    raise ValueError("scale.txt must contain exactly 3 integers (nx ny nz)")

nx, ny, nz = scales
print("Scaling factors:", nx, ny, nz)

# Identify non-scaled direction (should be 1)
scale_vec = np.array([nx, ny, nz])
perp_dir = np.where(scale_vec == 1)[0]

#if len(perp_dir) != 1:
#    raise ValueError("Exactly ONE direction must be unscaled for nanotube mapping.")

perp = perp_dir[0]
print(f"Perpendicular (non-scaled) direction: {perp}")

L_perp = np.linalg.norm(cell[perp])

# ----------------------------
# Mode selection
# ----------------------------
mode = input("0 = nanotube, 1 = nanoscroll: ").strip()

k = int(input("k = +1 or -1: ").strip())

# ----------------------------
# Nanotube parameters
# ----------------------------
if mode == "0":
    print("\n--- NANOTUBE MODE ---")

    # radius from geometry (projected in-plane area scale)
    a = cell[0]
    b = cell[1]
    arg = np.linalg.norm(a + b) / (2 * np.pi)

    R = arg

    new_positions = []

    for r in positions:
        x0, y0, z0 = r

        # corrected radius expression
        radius = R + ((1 - k) / 2.0) * L_perp + k * z0

        theta = -2.0*k * x0 / R

        x1 = radius * np.cos(theta)
        y1 = radius * np.sin(theta)
        z1 = -y0

        new_positions.append([x1, y1, z1])

# ----------------------------
# Nanoscroll
# ----------------------------
elif mode == "1":
    print("\n--- NANOSCROLL MODE ---")

    w = int(input("w = +1 or -1: ").strip())
    r0 = float(input("r0 (inner radius): ").strip())
    s = float(input("spiral parameter s: ").strip())

    s0 = r0**2 / 2.0

    new_positions = []

    for r in positions:
        x0, y0, z0 = r

        u = np.sqrt(2 * s * (x0 + s0))

        radius = u + ((1 - k) / 2.0) * L_perp + k * z0
        angle = -w * np.sqrt(2 * (x0 + s0) / s)

        x1 = radius * np.cos(angle)
        y1 = radius * np.sin(angle)
        z1 = -y0

        new_positions.append([x1, y1, z1])

else:
    raise ValueError("Mode must be 0 (nanotube) or 1 (nanoscroll)")

# ----------------------------
# Update structure
# ----------------------------
atoms.set_positions(np.array(new_positions))

# ----------------------------
# Write output POSCAR
# ----------------------------
write("POSCAR_nanostructure", atoms, format="vasp", direct=False)

print("\nDONE → POSCAR_nanostructure written")
print("Atoms:", len(atoms))
