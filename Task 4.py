#Skeleton Program code for the AQA A Level Paper 1 Summer 2024 examination
#this code should be used in conjunction with the Preliminary Material
#written by the AQA Programmer Team
#developed in the Python 3.9.4 programming environment

# What you need to do
# Task 4.1
# Modify the constructor in the Puzzle class to pass an additional parameter (random between 1 and 3
# inclusive) for each pattern when it is instantiated. This is the number of each pattern which can be placed
# as described.
# Task 4.2
# Modify the Pattern class to use this additional parameter to limit the number of patterns which can be
# placed into the Grid. Store this value in a new property called PatternCount. You only need to place
# restrictions on a standard puzzle. PatternCount for the associated pattern should be decremented as
# each valid pattern is placed.
# Task 4.3
# Create a new method OutputPatternCount in the Pattern class which displays an appropriate message
# onto the screen stating the limit for each pattern type.
# Task 4.4
# Test that the changes you have made work:
# ● Run the Skeleton Program.
# ● Press enter to create a standard puzzle.
# ● Show the program displaying the number of each pattern type available.
# ● Input a T pattern at a suitable location.
# ● Show the program displaying the reduction in the number of T pattern types available.
# ● Repeat the above to use all the T patterns available.
# ● Show the program giving a suitable error message when the user attempts to place a T symbol.

import random
import os

random.seed(10)

def Main():
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        if len(args) == 1:
            self.__Score = 0
            self.__SymbolsLeft = 0
            self.__GridSize = 0
            self.__Grid = []
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            self.__LoadPuzzle(args[0])
        else:
            self.__Score = 0
            self.__SymbolsLeft = args[1]
            self.__GridSize = args[0]
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    C = Cell()
                else:
                    C = BlockedCell()
                self.__Grid.append(C)
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
            QPattern = Pattern("Q", "QQ**Q**QQ", random.randrange(1, 4))
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X", random.randrange(1, 4))
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T", random.randrange(1, 4))
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")
            BPattern = Pattern("B", "B*B*B*B*B", random.randrange(1, 4))
            self.__AllowedPatterns.append(BPattern)
            self.__AllowedSymbols.append("B")

    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())
                for Count in range (1, NoOfSymbols + 1):
                    self.__AllowedSymbols.append(f.readline().rstrip())
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                self.__GridSize = int(f.readline().rstrip())
                for Count in range (1, self.__GridSize * self.__GridSize + 1):
                    Items = f.readline().rstrip().split(",")
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        for CurrentSymbol in range(1, len(Items)):
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                self.__SymbolsLeft = int(f.readline().rstrip())
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            self.DisplayPuzzle()
            print("Current score: " + str(self.__Score))
            Row = -1
            Valid = False
            # ● Show the program displaying the number of each pattern type available. 
            for p in self.__AllowedPatterns:
                p.OutputPatternCount()
            
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    pass
            Column = -1
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            Symbol = self.__GetSymbolFromUser()
            self.__SymbolsLeft -= 1
            print(self.__Grid)
            CurrentCell = self.__GetCell(Row, Column)
            if CurrentCell.CheckSymbolAllowed(Symbol):
                CurrentCell.ChangeSymbolInCell(Symbol)
                AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                if AmountToAddToScore > 0:
                    self.__Score += AmountToAddToScore
            print(f"{self.__SymbolsLeft = }")
            if self.__SymbolsLeft == 0:
                Finished = True
        self.DisplayPuzzle()
        print()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()
 
    # def __GetCell(self, row, column):
    #     # Calculate the reverse row number (starting from the bottom)
    #     reverse_row = self.__GridSize - row

    #     # Calculate the starting index of the desired row in the grid
    #     row_start_index = reverse_row * self.__GridSize

    #     # Adjust the column index to be zero-based
    #     adjusted_column_index = column - 1

    #     # Calculate the final index for the cell in the one-dimensional grid list
    #     index = row_start_index + adjusted_column_index

    #     # Return the cell at the calculated index
    #     if index >= 0:
    #         return self.__Grid[index]
    #     else:
    #         raise IndexError("Index out of bounds")
    
    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                print(f"{StartRow = }, {StartColumn = } ")
                try:
                    # Create pattern string using list comprehension
                    positions = [
                        (StartRow, StartColumn), (StartRow, StartColumn + 1), 
                        (StartRow, StartColumn + 2), (StartRow - 1, StartColumn + 2), 
                        (StartRow - 2, StartColumn + 2),
                        (StartRow - 2, StartColumn + 1), (StartRow - 2, StartColumn),
                        (StartRow - 1, StartColumn), (StartRow - 1, StartColumn + 1)
                    ]
                    PatternString = "".join(self.__GetCell(r, c).GetSymbol() for r, c in positions)

                    # Print pattern string (for debugging purposes, can be removed in production)
                    print(f"{PatternString = }")

                    # Check pattern against allowed patterns
                    for i in range(len(self.__AllowedPatterns)):
                        P = self.__AllowedPatterns[i]
                        print(f"{P = }")  # Print pattern (for debugging, can be removed)
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol) and self.__AllowedPatterns[i].GetPatternCount() > 0:
                            # Add current symbol to not allowed symbols for all cells in the pattern
                            self.__AllowedPatterns[i].DecreasePatternCount()
                            for r, c in positions:
                                self.__GetCell(r, c).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                except IndexError:
                    # Skip this pattern check if out of grid bounds
                    pass
        return 0

    def __GetSymbolFromUser(self):
        Symbol = ""
        while not Symbol in self.__AllowedSymbols:
            Symbol = input("Enter symbol: ")
        return Symbol

    def __CreateHorizontalLine(self):
        Line = "  "
        for Count in range(1, self.__GridSize * 2 + 2):
            Line = Line + "-"
        return Line

    def DisplayPuzzle(self):
        print()
        if self.__GridSize < 10:
            print("  ", end='')
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
        print(self.__CreateHorizontalLine())
        
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

    
class Pattern():
    def __init__(self, SymbolToUse, PatternString, PatternCount):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString
        self.__PatternCount = PatternCount

    def MatchesPattern(self, PatternString, SymbolPlaced):
        if SymbolPlaced != self.__Symbol:
            return False
        for Count in range(0, len(self.__PatternSequence)):
            try:
                if self.__PatternSequence[Count] == self.__Symbol and PatternString[Count] != self.__Symbol:
                    return False
            except Exception as ex:
                print(f"EXCEPTION in MatchesPattern: {ex}")
        return True

    # CHANGES START HERE
    
    def DecreasePatternCount(self):
        self.__PatternCount -= 1

    def GetPatternCount(self):
        return self.__PatternCount

    # Create a new method OutputPatternCount in the Pattern class which displays an appropriate message
    # onto the screen stating the limit for each pattern type.

    def OutputPatternCount(self):
        print(f"Limit for {self.__Symbol} is {self.__PatternCount}")

    # CHANGES END HERE
    
    def GetPatternSequence(self):
      return self.__PatternSequence

    def __str__(self):
        return f"{self.__Symbol}: {self.__PatternSequence}"

    def __repr__(self):
        return f"{self.__Symbol}: {self.__PatternSequence}"

class Cell():
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        if self.IsEmpty():
          return "-"
        else:
          return self._Symbol

    def IsEmpty(self):
        if len(self._Symbol) == 0:
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        for Item in self.__SymbolsNotAllowed:
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

    # Dunder Method
    def __str__(self):
        return self._Symbol

    # Dunder Method
    def __repr__(self):
        return self._Symbol

class BlockedCell(Cell):
    def __init__(self):
        super(BlockedCell, self).__init__()
        self._Symbol = "@"

    # Overriding the method from original parental class "Cell"
    def CheckSymbolAllowed(self, SymbolToCheck):
        return False

if __name__ == "__main__":
    Main()
