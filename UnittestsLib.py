import numpy as np
import sys
import pstats

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
        p = pstats.Stats(Filename)
        p.strip_dirs().sort_stats(Key).print_stats(*restrictions)

    def test_chefAndWells(self, SaveName, *chefAndWellsArgs):
        from VillageAndWells import Solution
        sol = Solution()
        res = sol.chefAndWells(*chefAndWellsArgs)
        # for el in res:
        #     for c in el:
        #         print(c, end=" ")
        #     print()
    def test_get_WellCoordinates(self):

        pass




