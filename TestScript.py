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
    # sol.set_PrerequisiteAttributes()
    Unittest.profile_CPU(sol.chefAndWells, ny, nx, VillageMap)

    # get_WellCoordinates
    Unittest.test_get_WellCoordinates(sol, ny, nx, VillageMap)
