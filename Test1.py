import numpy as np
import sys
import cProfile
import pstats
import __main__
from VillageAndWells import Solution

n = m = 100
# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}
VillageComponents = np.array(["H", "W", ".", "N"])
ProfileCPU = True
SaveName = 'VillageAndWells'
DumpName = SaveName + '.prof'

def PrintDump(Filename, *restrictions, Key = 'cumulative'):
    p = pstats.Stats(Filename)
    p.strip_dirs().sort_stats(Key).print_stats(*restrictions)

def CreateRandomVillage(n, m):
    rng = np.random.default_rng(seed = 202305)
    VillageMap = rng.choice( VillageComponents,  size = (n,m) )
    Print2DArray(VillageMap)
    return VillageMap

def Print2DArray(a):
    print("\n Generated a random village ")
    np.savetxt(sys.stdout.buffer, a, fmt='%s')



if __name__=="__main__":
    VillageMap = CreateRandomVillage(n, m)
    obj = Solution()
    prof = cProfile.Profile()
    prof.enable()
    res = obj.chefAndWells(n, m, VillageMap)
    prof.disable()
    prof.dump_stats(DumpName)
    PrintDump(DumpName, Key = 'tottime')
    print("{:} success".format(__main__.__file__))
    
    # for el in res:
    #     for c in el:
    #         print(c, end=" ")
    #     print()