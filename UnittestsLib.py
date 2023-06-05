import numpy as np
import sys
import pstats
import cProfile

# not sure if we should keep the Solution object through all tests or create a new one for each


# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}

class Unittests:
    def __init__(self) -> None:
        self.VillageComponents = np.array(["H", "W", ".", "N"])
    def CreateRandomVillage(self, n, m):
        rng = np.random.default_rng(seed = 202305)
        VillageMap = rng.choice( self.VillageComponents,  size = (n,m) )
        self.Print2DArray(VillageMap)
        return VillageMap
    def Print2DArray(self, a):
        print("\n Generated a random village ")
        np.savetxt(sys.stdout.buffer, a, fmt='%s')
    def PrintDump(self, Filename, *restrictions, Key = 'cumulative'):
        """print profiling data by reading Filename"""
        p = pstats.Stats(Filename)
        p.strip_dirs().sort_stats(Key).print_stats(*restrictions)
    def profileCPUUsageOfFunction(self, FunctionHandle, *args):
        """use cProfile to profile the CPU usage of FunctionHandle"""
        SaveName = FunctionHandle.__name__
        prof = cProfile.Profile()
        prof.enable()
        res = FunctionHandle(*args)
        prof.disable()
        self.outputProfilingData(prof, SaveName)
        return res
    def outputProfilingData(self, prof, SaveName):
        """output the profiling data as a file and in the terminal"""
        DumpName = SaveName + '.prof'
        prof.dump_stats(DumpName)
        self.PrintDump(DumpName, Key = 'tottime')
        print("{:} success".format(SaveName))
    def testgetWellSquares(self, sol):
        sol.getWellSquares()
    def testUpdateVisitedSquares(self, sol):
        sol.initializeCurrentSquares()
        sol.updateVisitedSquares()
        print(sol.VisitedSquares)
        print("(0,7) is in VisitedSquares", (0,7) in sol.VisitedSquares)
        print("(0,7) is in VisitedSquares", (0,0) in sol.VisitedSquares)
    # def testCalculateTravelDistances(self, sol):
        # sol.setNonHouseDistances()
        # print(self.TravelDistances)
    def testGeneralFunction(self, FunctionHandle, *args, **kwargs):
        res = FunctionHandle(*args, **kwargs)
        print(res)
        return res
        







