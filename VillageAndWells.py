# H House 2
# W Well 3
# . open ground 1
# N prohibited 0

# need to optimize
# for optimization, we realize that only the first TravelStep allows traveling in all directions
# afterwards the pointy ends allow 3 directions while the side branches only allow 2-3 directions
# create NewPositions by creating shifted Index arrays?
# or Map the occupied squares and iterate? Mask then loop?
# use a hashset. hashtable in python is a dictionary. hashset has no key-value pair and is unordered, pretty much a list of unique elements where you can check the existence of elements very fast
# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}
# 5 5
# N H N . H
# N N W . N
# N H N H .
# N W . W .
# H H W . W


from typing import List
import numpy as np





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
        self.TravelDistances = np.ones((self.n, self.m), dtype=int)*(-1)

    # we realize that going back and forth starting from a well is the same as starting from a house
    # suppose we find a shortest route between a house and a well, then the corresponding sections of the route are also the shortest routes for houses along the route
    # we further realize that we can find all possible routes of length n by travelling from the current location in all 4 directions. Of course travelling to already visited positions(including the previous one) is useless. What about the case when two people want to move on to the same square? It does not matter, since both have travelled the same distance. We save the TravelledDistance in a separate matrix. We can even create a PreviousLocation matrix from which we can recursively obtain a shortest route. 
    # It would be great if we could visualize the progression of TravelledDistance

    def chefAndWells(self, n : int, m : int, c : List[List[str]]) -> List[List[int]]:
        self.set_n(n)
        self.set_m(m)
        self.set_VillageMap(c)
        self.InitializeTravelDistance()
        self.Positions = self.ResetPositions() # Counter for how many squares are occupied right now
        NumberOfWells = self.FindWells()
        self.nPositions = NumberOfWells # Number of currently occupied squares
        while self.nPositions>0:
            # print("npositions: ", self.nPositions)
            self.TravelledDistance += 2
            self.Travel()
            self.SetOpenProhibitedDistances()
            # print("Positions\n", self.Positions)
            # print("TravelDistance after: \n", self.TravelDistances)
        self.CleanUp()
        return self.TravelDistances



    def Travel(self):
        NewPositions = self.ResetPositions()
        # nDummyCurrentPositions = self.nPositions # Counter for how many squares are occupied right now
        nNewPositions = 0
        # print("coordinates before travelling")
        for i in range(self.nPositions):
            # print(self.Positions[:,i])
            LocalPositions, nLocalPositions = self.TravelLocal(self.Positions[:,i])
            # print("nlocalpositions: ", nLocalPositions)
            for j in range(nLocalPositions):
                NewPositions[0][nNewPositions + j] = LocalPositions[0][j]
                NewPositions[1][nNewPositions + j] = LocalPositions[1][j]
            # print(NewPositions)
            # self.UpdateTravelDistanceLocal(nLocalPositions, LocalPositions)
            nNewPositions += nLocalPositions
        self.Positions = NewPositions
        self.nPositions = nNewPositions
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
        # >0 or >-1 are both fine at first since there should be no secondary Travel from a well. Meaning, We travel from all wells. Once a route funnels into another well (which is only possible if two wells are side by side), there is no need to travel further since any other route is longer
        # >0 ensures no conflict(unwanted travelstop) when setting "." and "N" to 0. 
        if(self.TravelDistances[coords]>-1):
            return False
        elif(self.VillageMap[coords] == "N"):
            self.TravelDistances[coords]=0
            return False
        else:
            self.UpdateTravelDistance(*coords)
            return True
    def UpdateTravelDistanceLocal(self, nLocalPositions, LocalPositions):
        # print("TravelDistance before: ", self.TravelDistances)
        for i in range(nLocalPositions):
            self.TravelDistances[tuple(LocalPositions[:,i])] = self.TravelledDistance
        # print("TravelDistance after: ", self.TravelDistances)
    def UpdateTravelDistance(self, *coords):
        self.TravelDistances[coords] = self.TravelledDistance

    def CleanUp(self):
        # assign TravelDistances 0 to all remaining N and .
        # need a filter to avoid looping through the whole array again?
        self.FindOpenProhibited()

    def ResetPositions(self):
        return np.ones( (2,self.n*self.m), dtype=int )*(-1)

    def FindOpenProhibited(self):
        Mask = ( ((self.VillageMap == "N") | (self.VillageMap == ".")) & (self.TravelDistances == -1 ) )
        rows, cols = np.indices((self.n,self.m))
        rows, cols = rows[Mask], cols[Mask]
        NSquares = len(rows)
        for i in range(NSquares):
            coords = rows[i], cols[i]
            # set TravelDistances to 0 for N and .
            self.TravelDistances[coords] = 0
    # first, get the indices of the wells
    def FindWells(self):
        Mask = (self.VillageMap == "W")
        rows, cols = np.indices((self.n,self.m))
        rows, cols = rows[Mask], cols[Mask]
        NumberOfWells = len(rows)
        # Traveldistance starting from well is 0, occupy the Wells
        for i in range(NumberOfWells):
            coords = rows[i], cols[i]
            self.TravelDistances[coords] = 0
            self.Positions[0][i] = rows[i]
            self.Positions[1][i] = cols[i]
        return NumberOfWells
    def SetOpenProhibitedDistances(self):
        # as per challenge, Traveldistance from N or . are defined as 0. Not sure if I agree. Could detach this part...
        for i in range(self.nPositions):
            coords = tuple(self.Positions[:,i])
            # print("coords", coords)
            # print(self.VillageMap[CurrentPosition])
            if( (self.VillageMap[coords] == 'N') or (self.VillageMap[coords] == '.') ):
                # print("its N or .")
                # print(coords, "setting Traveldistances to 0")
                self.TravelDistances[coords] = 0








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