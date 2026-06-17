import numpy as np
from ase.io import read, write

# ----------------------------
# INPUT / OUTPUT
# ----------------------------
input_file = "POSCAR_nanostructure"
output_file = "POSCAR_nanotube"

# ----------------------------
# READ STRUCTURE
# ----------------------------
atoms = read(input_file)

print("\nReading:", input_file)
print("Atoms:", len(atoms))

# ----------------------------
# CLEAN POSITIONS
# ----------------------------
pos = atoms.get_positions()

# remove numerical noise (VERY important after trig transforms)
pos = np.round(pos, 8)

atoms.set_positions(pos)

# ----------------------------
# OPTIONAL: RECENTER STRUCTURE
# (useful for visualization stability)
# ----------------------------
center = pos.mean(axis=0)
atoms.translate(-center)

# ----------------------------
# OPTIONAL: WRAP POSITIONS
# (keeps coordinates compact)
# ----------------------------
atoms.wrap()

# ----------------------------
# WRITE FINAL POSCAR
# ----------------------------
write(output_file, atoms, format="vasp", direct=False)

print("\nDONE →", output_file)
