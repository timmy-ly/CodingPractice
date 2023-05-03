import numpy as np
import sys

n = m = 3

def CreateRandomVillage(n, m):
    rng = np.random.default_rng(seed = 202305)
    VillageMap = rng.choice( VillageComponents,  size = (n,m) )
    Print2DArray(VillageMap)
    return VillageMap

def Print2DArray(a):
    print("\n Generated a random village ")
    np.savetxt(sys.stdout.buffer, a, fmt='%s')

# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}
VillageComponents = np.array(["H", "W", ".", "N"])
VillageMap = CreateRandomVillage(n, m)

