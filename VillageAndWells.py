# H House 2
# W Well 3
# . open ground 1
# N prohibited 0

# we realize that going back and forth starting from a well is the same as starting from a house
# suppose we find a shortest route between a house and a well, then the corresponding sections of the route are also the shortest routes for houses along the route
# we further realize that we can find all possible routes of length Ny by travelling from the current location in all 4 directions. Of course travelling to already visited positions(including the previous one) is useless. What about the case when two people want to move on to the same square? It does not matter, since both have travelled the same distance. We save the CurrentTravelDistance in a separate matrix. We can even create a PreviousLocation matrix from which we can recursively obtain a shortest route. 
# It would be great if we could visualize the progression of CurrentTravelDistance

# need to optimize
# for optimization, we realize that only the first TravelStep allows traveling in all directions
# afterwards the pointy ends allow 3 directions while the side branches only allow 2-3 directions
# try bulk creating neighboring Squares...what about the boundaries?
# create difference set with VisitedSquares
# loop through difference set and check for boundaries? maybe use np.where
# I think a combination of arrays and hashsets is possible
# also I am pretty sure that it would be much easier to use 1d integer coordinates instead of tuples, just the input and output needs to reshaped
#i.e., sth. like iy*Nx + ix

# my code fails on test 1115, probably due to python/numpy version differences. I dont care about the old versions so I'm satisfied with this one

# use a hashset. hashtable in python is a dictionary. hashset has no key-value pair and is unordered, pretty much a list of unique elements where you can check the existence of elements very fast



from typing import List
import numpy as np



def convertSetOfTuplesTo2DArray(SetOfTuples):
    return np.array(list(SetOfTuples))
def convert2DArrayToSetOfTuples(Array):
    return set(zip(Array[:,0], Array[:,1]))

class Solution:
    """Class for solving the village and wells problem, mainly for scope"""
    def __init__(self) -> None:
        self.Ny = 0
        self.Nx = 0
        self.c = None
        self.CurrentTravelDistance = 0 # current CurrentTravelDistance
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
        # print(self.TravelDistances)
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
        while self.CurrentSquares:
            # print(self.CurrentSquares)
            self.CurrentTravelDistance += 2
            self.travel()
            self.updateTravelDistances()
            # self.Travel(CurrentSquares)
            # self.SetOpenProhibitedDistances()
            self.updateVisitedSquares(self.CurrentSquares)
        self.setNonHouseDistances()

    def travel(self):
        PreviousSquares = convertSetOfTuplesTo2DArray(self.CurrentSquares)
        RightSquares = PreviousSquares.copy()
        LeftSquares = PreviousSquares.copy()
        UpSquares = PreviousSquares.copy()
        DownSquares = PreviousSquares.copy()
        RightSquares[:,1] +=1
        LeftSquares[:,1] -=1
        UpSquares[:,0] -=1
        DownSquares[:,0] +=1
        RightSquares = convert2DArrayToSetOfTuples(RightSquares)
        LeftSquares = convert2DArrayToSetOfTuples(LeftSquares)
        UpSquares = convert2DArrayToSetOfTuples(UpSquares)
        DownSquares = convert2DArrayToSetOfTuples(DownSquares)
        NonUniqueCurrentSquares = RightSquares | LeftSquares | UpSquares | DownSquares
        self.CurrentSquares = NonUniqueCurrentSquares - self.VisitedSquares
        self.checkBoundaries()
    def checkBoundaries(self):
        CurrentSquaresUncheckedBounds = self.CurrentSquares.copy()
        for Square in CurrentSquaresUncheckedBounds:
            if(Square[0]>=self.Ny or Square[0]<0 or Square[1]>=self.Nx or Square[1]<0):
                self.CurrentSquares.remove(Square)
    def travelSlowly(self):
        """Advance Branches in all directions starting from CurrentSquares"""
        PreviousSquares = self.CurrentSquares.copy()
        self.CurrentSquares.clear()
        for Square in PreviousSquares:
            self.travelLocally(Square)
        
    def travelLocally(self, Square):
        self.travelRight(Square)
        self.travelLeft(Square)
        self.travelUp(Square)
        self.travelDown(Square)
        # need to think about boundary check and VisitedSquares check?
    def travelRight(self, Square): 
        NewSquare = tuple(np.add(Square, (0,1)))
        if( (NewSquare not in self.VisitedSquares) and (not self.isOutOfRightBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelLeft(self, Square): 
        NewSquare = tuple(np.add(Square, (0,-1)))
        if( (NewSquare not in self.VisitedSquares) and (not self.isOutOfLeftBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelUp(self, Square): 
        NewSquare = tuple(np.add(Square, (-1,0)))
        if( (NewSquare not in self.VisitedSquares) and (not self.isOutOfTopBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def travelDown(self, Square): 
        NewSquare = tuple(np.add(Square, (1,0)))
        if( (NewSquare not in self.VisitedSquares) and (not self.isOutOfBottomBoundary(NewSquare)) ):
            self.CurrentSquares.add(NewSquare)
    def isOutOfRightBoundary(self, Square):
        return Square[1]>=self.Nx
    def isOutOfLeftBoundary(self, Square):
        return Square[1]<0
    def isOutOfTopBoundary(self, Square):
        return Square[0]<0
    def isOutOfBottomBoundary(self, Square):
        return Square[0]>=self.Ny
    def updateTravelDistances(self):
        for Square in self.CurrentSquares:
            self.TravelDistances[Square] = self.CurrentTravelDistance
    def updateVisitedSquares(self, Squares):
        """add Squares to the VisitedSquares"""
        self.VisitedSquares.update(Squares)
    def setNonHouseDistances(self):
        Mask = ((self.VillageMap == "W") | (self.VillageMap == "N") | (self.VillageMap == "."))
        self.TravelDistances = np.where(Mask, 0, self.TravelDistances)














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