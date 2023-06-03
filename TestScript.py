# import numpy as np
import cProfile
from VillageAndWells import Solution
from UnittestsLib import Unittests

ny = nx = 100
ProfileCPU = True
SaveName = 'VillageAndWells'
DumpName = SaveName + '.prof'




# I guess a proper unittest needs an exception catcher somewhere
if __name__=="__main__":
    # main
    Unittest = Unittests()
    VillageMap = Unittest.CreateRandomVillage(ny, nx)
    prof = cProfile.Profile()
    prof.enable()
    Unittest.test_chefAndWells(SaveName, ny, nx, VillageMap)
    prof.disable()
    prof.dump_stats(DumpName)
    Unittest.PrintDump(DumpName, Key = 'tottime')
    print("{:} success".format(SaveName))
    # get_WellCoordinates
