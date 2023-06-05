# import numpy as np
import cProfile
from VillageAndWells import *
from UnittestsLib import Unittests

Ny = Nx = 10
ProfileCPU = True
SaveName = 'VillageAndWells'
DumpName = SaveName + '.prof'
Unittest = Unittests()
VillageMap = Unittest.CreateRandomVillage(Ny, Nx)
sol = Solution()
sol.setPrerequisiteAttributes(Ny, Nx, VillageMap)



if __name__=="__main__":
    # main
    # sol.set_PrerequisiteAttributes()
    # Unittest.profileCPUUsageOfFunction(sol.chefAndWells, Ny, Nx, VillageMap)

    # get_WellCoordinates
    # Unittest.testgetWellSquares(sol)
    # Unittest.testUpdateVisitedSquares(sol)
    a = np.arange(10)
    a = np.reshape(a, (5,2))
    b = Unittest.testGeneralFunction(convert2DArrayToSetOfTuples, a)
    c = Unittest.testGeneralFunction(convertSetOfTuplesTo2DArray, b)

# 