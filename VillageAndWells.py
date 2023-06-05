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
# might have been better to use 1d coordinates, i.e., sth. like iy*Nx + ix
# Legend = {"H": 2, "W": 3, ".": 1, "N": 0}
# 5 5
# N H N . H
# N N W . N
# N H N H .
# N W . W .
# H H W . W


from typing import List
import numpy as np


def convertSetOfTuplesTo2DArray(SetOfTuples):
    return np.array(list(SetOfTuples))
def convert2DArrayToSetOfTuples(Array):
    return set(zip(Array[:,0], Array[:,1]))

def reset_Coords(Ny,Nx):
    return np.ones( (2,Ny*Nx), dtype=int )*(-1)

# class SetOfSquares:
# # A set of squares that share the TravelledDistance
#     def __init__(self, Ny, Nx, TravelledDistance) -> None:
#         self.Ny, self.Nx = Ny, Nx
#         self.Coords = reset_Coords(Ny,Nx) 
#         self.TravelledDistance = self.set_TravelledDistance(TravelledDistance)
#         self.Amount = 0
#     def set_TravelledDistance(self, TravelledDistance):
#         self.TravelledDistance = TravelledDistance
#     def set_Size(self, Amount):
#         self.Amount = Amount
class Solution:
    """Class for solving the village and wells problem, mainly for scope"""
    def __init__(self) -> None:
        self.Ny = 0
        self.Nx = 0
        self.c = None
        self.TravelledDistance = 0 # current travelleddistance
        self.AmountOfWells = 0
        self.VisitedSquares = set()
    def chefAndWells(self, Ny : int, Nx : int, VillageMap : List[List[str]]) -> List[List[int]]:
        """Main method which solves the village and wells problem"""
        self.setPrerequisiteAttributes(Ny, Nx, VillageMap)
        self.initializeTravelDistances()
        self.initializeCurrentSquares()
        self.updateVisitedSquares(self.CurrentSquares)
        self.addProhibitedToVisitedSquares()

        self.calculateTravelDistances()
        # self.CleanUp()
        return self.TravelDistances
    def setPrerequisiteAttributes(self, Ny, Nx, VillageMap):
        self.setNy(Ny)
        self.setNx(Nx)
        self.setVillageMap(VillageMap)
        # self.setAllCoordinates()
    def setNy(self,Ny):
        """set the y-length of the village map"""
        self.Ny = Ny
    def setNx(self,Nx):
        """set the x-length of the village map"""
        self.Nx = Nx
    def setVillageMap(self, VillageMap):
        """set the VillageMap attribute by transforming the list input into an array"""
        self.VillageMap = np.array(VillageMap)
    # def setAllCoordinates(self):
        # self.AllCoordinates = np.indices((self.Ny,self.Nx))
    def initializeTravelDistances(self):
        """initialize array of shape (Ny,Nx) with -1 entries to signify that non of the squares have been travelled to yet. Also serves as inaccessible squares at the end"""
        self.TravelDistances = np.ones((self.Ny, self.Nx), dtype=int)*(-1)
    def initializeCurrentSquares(self):
        """get the [x,y] coordinates of the wells and allocate them to the 2D array CurrentSquares"""
        self.CurrentSquares = self.getSquaresOfType("W")
    def getSquaresOfType(self, SquareType):
        """"use numpy mask to find where the squares of type SquareType are in VillageMap. Get their indices with nonzero and add each (y,x) coordinate pair to a set"""
        Mask = (self.VillageMap == SquareType)
        Indices = Mask.nonzero()
        Indices = set(zip(Indices[0], Indices[1]))
        return Indices
    def addProhibitedToVisitedSquares(self):
        """Since we wont travel further from prohibted squares "N", we can directly add them to the VisitedSquares"""
        ProhibitedSquares = self.getSquaresOfType("N")
        self.updateVisitedSquares(ProhibitedSquares)
    def calculateTravelDistances(self):
        """main algorithm"""
        i = 0
        while i<1:
            self.travel()
            # self.TravelledDistance += 2
            # self.Travel(CurrentSquares)
            # self.SetOpenProhibitedDistances()
            self.updateVisitedSquares(self.CurrentSquares)
            i +=1
        self.setNonHouseDistances()
    def updateVisitedSquares(self, Squares):
        """add Squares to the VisitedSquares"""
        self.VisitedSquares.update(Squares)
    def travel(self):
        PreviousSquares = self.CurrentSquares
        self.clearCurrentSquares()
        for Square in PreviousSquares:
            self.travelLocally(Square)
        self.updateTravelledDistances()
        
    def clearCurrentSquares(self):
        self.CurrentSquares = set()
    def travelLocally(self, Square):
        self.travelRight(Square)
        self.travelLeft(Square)
        self.travelUp(Square)
        self.travelDown(Square)
        # need to think about boundary check and VisitedSquares check?
    def travelRight(self, Square): 
        NewSquare = np.add(Square, (0,1))
        if( (NewSquare not in self.VisitedSquares) or (not self.isOutOfRightBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelLeft(self, Square): 
        NewSquare = np.add(Square, (0,-1))
        if( (NewSquare not in self.VisitedSquares) or (not self.isOutOfLeftBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelUp(self, Square): 
        NewSquare = np.add(Square, (-1,0))
        if( (NewSquare not in self.VisitedSquares) or (not self.isOutOfTopBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelDown(self, Square): 
        NewSquare = np.add(Square, (1,0))
        if( (NewSquare not in self.VisitedSquares) or (not self.isOutOfBottomBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def isOutOfRightBoundary(self, Square):
        return Square[1]>=self.Ny
    def isOutOfLeftBoundary(self, Square):
        return Square[1]<0
    def isOutOfTopBoundary(self, Square):
        return Square[0]<0
    def isOutOfBottomBoundary(self, Square):
        return Square[0]>=self.Nx
    def updateTravelledDistances(self):
        for Square in self.CurrentSquares:
            pass

    def setNonHouseDistances(self):
        Mask = ((self.VillageMap == "W") | (self.VillageMap == "N") | (self.VillageMap == "."))
        self.TravelDistances = np.where(Mask, 0, self.TravelDistances)


        

        

    


    # we realize that going back and forth starting from a well is the same as starting from a house
    # suppose we find a shortest route between a house and a well, then the corresponding sections of the route are also the shortest routes for houses along the route
    # we further realize that we can find all possible routes of length Ny by travelling from the current location in all 4 directions. Of course travelling to already visited positions(including the previous one) is useless. What about the case when two people want to move on to the same square? It does not matter, since both have travelled the same distance. We save the TravelledDistance in a separate matrix. We can even create a PreviousLocation matrix from which we can recursively obtain a shortest route. 
    # It would be great if we could visualize the progression of TravelledDistance





    def Travel(self, CurrentSquares):
        NewPositions = reset_Coords(self.Ny,self.Nx)
        # nDummyCurrentPositions = self.NumberCurrentlyOccupiedSquares # Counter for how many squares are occupied right now
        nNewPositions = 0
        # print("coordinates before travelling")
        for i in range(CurrentSquares.Amount):
            # print(self.SetOfSquares[:,i])
            LocalPositions, nLocalPositions = self.TravelLocal(CurrentSquares.Coords[:,i])
            # print("nlocalpositions: ", nLocalPositions)
            for j in range(nLocalPositions):
                NewPositions[0][nNewPositions + j] = LocalPositions[0][j]
                NewPositions[1][nNewPositions + j] = LocalPositions[1][j]
            # print(NewPositions)
            # self.UpdateTravelDistanceLocal(nLocalPositions, LocalPositions)
            nNewPositions += nLocalPositions
        CurrentSquares.Coords = NewPositions
        CurrentSquares.Amount = nNewPositions
    def TravelLocal(self, CurrentPosition):
        row, col = CurrentPosition
        nNewPositions = 0
        NewPositions = np.ones( (2,4), dtype=int )*(-1)
        # go right
        if(col < self.Nx-1):
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
        if(row < self.Ny-1):
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



    def FindOpenProhibited(self):
        Mask = ( ((self.VillageMap == "N") | (self.VillageMap == ".")) & (self.TravelDistances == -1 ) )
        rows, cols = np.indices((self.Ny,self.Nx))
        rows, cols = rows[Mask], cols[Mask]
        NSquares = len(rows)
        for i in range(NSquares):
            coords = rows[i], cols[i]
            # set TravelDistances to 0 for N and .
            self.TravelDistances[coords] = 0
    # first, get the indices of the wells

    def get_Wells_old(self):
        Mask = (self.VillageMap == "W")
        Coords = {}
        rows, cols = np.indices((self.Ny,self.Nx))
        rows, cols = rows[Mask], cols[Mask]
        self.AmountOfWells = len(rows)
        # Traveldistance starting from well is 0, occupy the Wells
        for i in range(self.AmountOfWells):
            CoordsSingle = rows[i], cols[i]
            self.TravelDistances[CoordsSingle] = 0
            Coords.add(CoordsSingle)
        return Coords#############################################Last

    def SetOpenProhibitedDistances(self):
        # as per challenge, Traveldistance from N or . are defined as 0. Not sure if I agree. Could detach this part...
        for i in range(self.NumberCurrentlyOccupiedSquares):
            coords = tuple(self.SetOfSquares[:,i])
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
    def Input(self,Ny,Nx):
        matrix=[]
        #matrix input
        for _ in range(Ny):
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
    def Input(self,Ny,Nx):
        matrix=[]
        #matrix input
        for _ in range(Ny):
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
        
        Ny,Nx= map(int,input().split())
    
        
        
        c=StringMatrix().Input(Ny, Nx)
        
        obj = Solution()
        res = obj.chefAndWells(Ny, Nx, c)
        
        for el in res:
            for c in el:
                print(c, end=" ")
            print()


# } Driver Code Ends