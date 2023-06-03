# import numpy as np
import cProfile
from VillageAndWells import Solution
from UnittestsLib import Unittests

ny = nx = 10
ProfileCPU = True
SaveName = 'VillageAndWells'
DumpName = SaveName + '.prof'
Unittest = Unittests()
VillageMap = Unittest.CreateRandomVillage(ny, nx)
sol = Solution()




if __name__=="__main__":
    # main
    # prof = cProfile.Profile()
    # prof.enable()
    # Unittest.test_chefAndWells(sol, ny, nx, VillageMap)
    # prof.disable()
    # prof.dump_stats(DumpName)
    # Unittest.PrintDump(DumpName, Key = 'tottime')
    # print("{:} success".format(SaveName))

    # get_WellCoordinates
    Unittest.test_get_WellCoordinates(sol, ny, nx, VillageMap)
