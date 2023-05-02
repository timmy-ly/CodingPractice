#User function Template for python3
# H House 2
# W Well 3
# . open ground 1
# N prohibited 0
import numpy as np
import sys
from typing import List

# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}
VillageComponents = np.array(["H", "W", ".", "N"])
def CreateRandomVillage(n, m):
    rng = np.random.default_rng(seed = 202305)
    VillageMap = rng.choice( VillageComponents,  size = (n,m) )
    Print2DArray(VillageMap)
    return VillageMap

def Print2DArray(a):
    print("\n Generated a random village ")
    np.savetxt(sys.stdout.buffer, a, fmt='%s')

CreateRandomVillage(5,5)

class Solution:
    def __init__(self) -> None:
        self.n = 0
        self.m = 0
        self.c = None
        self.TravelledDistance = 0 # current travelleddistance

    def set_n(self,n):
        self.n = n
    def set_m(self,m):
        self.m = m
    def set_VillageMap(self, VillageMap):
        # I prefer numpy
        self.VillageMap = np.array(VillageMap)
    def InitializeTravelDistance(self):
        self.TravelDistance = np.ones((self.n, self.m), dtype=int)*(-1)

    # we realize that going back and forth starting from a well is the same as starting from a house
    # suppose we find a shortest route between a house and a well, then the corresponding sections of the route are also the shortest routes for houses along the route
    # we further realize that we can find all possible routes of length n by travelling from the current location in all 4 directions. Of course moving on to already covered positions(including the previous one) is useless. What about the case when two people want to move on to the same square? It does not matter, since both have travelled the same distance. We save the TravelledDistance in a separate matrix. We can even create a PreviousLocation matrix from which we can recursively obtain a shortest route. 
    # It would be great if we could visualize the progression of TravelledDistance
    def chefAndWells(self, n : int, m : int, c : List[List[str]]) -> List[List[int]]:
        self.set_n(n)
        self.set_m(m)
        self.set_VillageMap(c)
        self.InitializeTravelDistance()
        self.Positions = self.ResetPositions() # Counter for how many squares are occupied right now
        NumberOfWells = self.FindWells()
        self.nPositions = NumberOfWells # Number of currently occupied squares
        # print(self.Positions[0])
        self.Travel()
        print(self.Positions[0,:self.nPositions])
        print(self.VillageMap[self.Positions[0,:self.nPositions], self.Positions[1,:self.nPositions]])


    def Travel(self):
        NewPositions = self.ResetPositions()
        # nDummyCurrentPositions = self.nPositions # Counter for how many squares are occupied right now
        nNewPositions = 0
        print("coordinates before travelling")
        for i in range(self.nPositions):
            print(self.Positions[:,i])
            LocalPositions, nLocalPositions = self.TravelLocal(self.Positions[:,i])
            print("nlocalpositions: ", nLocalPositions)
            for j in range(nLocalPositions):
                NewPositions[0][nNewPositions + j] = LocalPositions[0][j]
                NewPositions[1][nNewPositions + j] = LocalPositions[1][j]
            print(NewPositions)
            nNewPositions += nLocalPositions
        self.Positions = NewPositions
        self.nPositions = nNewPositions

    
    def ResetPositions(self):
        return np.ones( (2,self.n*self.m), dtype=int )*(-1)
    # first, get the indices of the wells
    def FindWells(self):
        WellsMask = (self.VillageMap == "W")
        WellRow, WellCol = np.indices((self.n,self.m))
        WellRow, WellCol = WellRow[WellsMask], WellCol[WellsMask]
        NumberOfWells = len(WellRow)
        # Traveldistance starting from well is 0, occupy the Wells
        for i in range(NumberOfWells):
            coords = WellRow[i], WellCol[i]
            self.TravelDistance[coords] = 0
            self.Positions[0][i] = WellRow[i]
            self.Positions[1][i] = WellCol[i]
        return NumberOfWells
    def TravelLocal(self, CurrentPosition):
        row, col = CurrentPosition
        nNewPositions = 0
        NewPositions = np.ones( (2,4), dtype=int )*(-1)
        # go right
        if(col < self.m-1):
            NewCol = col + 1
            if(self.CheckValid(row, NewCol)):
                NewPositions[0, nNewPositions] = row
                NewPositions[1, nNewPositions] = NewCol
                nNewPositions += 1
        # go left
        if(col > 0):
            NewCol = col - 1
            if(self.CheckValid(row, NewCol)):
                NewPositions[0, nNewPositions] = row
                NewPositions[1, nNewPositions] = NewCol
                nNewPositions += 1
        # go up
        if(row > 0):
            NewRow = row - 1
            if(self.CheckValid(NewRow, col)):
                NewPositions[0, nNewPositions] = NewRow
                NewPositions[1, nNewPositions] = col
                nNewPositions += 1
        # go down
        if(row < self.n-1):
            NewRow = row + 1
            if(self.CheckValid(NewRow, col)):
                NewPositions[0, nNewPositions] = NewRow
                NewPositions[1, nNewPositions] = col
                nNewPositions += 1
        return NewPositions, nNewPositions
    



    def CheckValid(self, *coords):
        return True
        if(self.TravelDistance[coords]>-1):
            return True
        else:
            return False







#{ 
 # Driver Code Starts
#Initial Template for Python 3

class StringMatrix:
    def __init__(self) -> None:
        pass
    def Input(self,n,m):
        matrix=[]
        #matrix input
        for _ in range(n):
            matrix.append([i for i in input().split()])
        return matrix
    def Print(self,arr):
        for i in arr:
            for j in i:
                print(j,end=" ")
            print()



class IntMatrix:
    def __init__(self) -> None:
        pass
    def Input(self,n,m):
        matrix=[]
        #matrix input
        for _ in range(n):
            matrix.append([int(i) for i in input().strip().split()])
        return matrix
    def Print(self,arr):
        for i in arr:
            for j in i:
                print(j,end=" ")
            print()


if __name__=="__main__":
    # read how often the program is to be run...
    t = int(input())
    for _ in range(t):
        
        n,m= map(int,input().split())
    
        
        
        c=StringMatrix().Input(n, m)
        
        obj = Solution()
        res = obj.chefAndWells(n, m, c)
        
        for el in res:
            for c in el:
                print(c, end=" ")
            print()

# } Driver Code Ends