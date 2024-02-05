import random
import os

def Main(): #Initial interface
    Again = "y"
    Score = 0
    while Again == "y":
        Filename = input("Press Enter to start a standard puzzle or enter name of file to load: ")
        if len(Filename) > 0:
            MyPuzzle = Puzzle(Filename + ".txt")
        else:
            MyPuzzle = Puzzle(8, int(8 * 8 * 0.6))
            """
                int(8 * 8 * 0.6) == int(38.4) == 38
                args[0] = grid size
                args[1] = 60% of grid
                User will be able to fill in up to 60% of the grid before the puzzle ends
            """
        Score = MyPuzzle.AttemptPuzzle()
        print("Puzzle finished. Your score was: " + str(Score))
        Again = input("Do another puzzle? ").lower()

class Puzzle():
    def __init__(self, *args):
        #*args - variable number of positional arguments
        if len(args) == 1:
            #If only 1 argument is passed into the class - 5x5 GRID
            #Following attributes set to 0 - will be updated with data in text file
            self.__Score = 0
                #Attribute that stores current score
            self.__SymbolsLeft = 0
                #Attribute that stores number of attempts left
            self.__GridSize = 0
                #Attribute that stores grid size
            self.__Grid = []
            self.__AllowedPatterns = []
                #Attribute that stores array of patterns
            self.__AllowedSymbols = []
                #Attribute that stores array of allowed symbols
            self.__LoadPuzzle(args[0])
        else:
            #If multiple/no arguments are passed (IN THIS CASE, 2) - RANDOM 8x8 GRID
            self.__Score = 0
            self.__SymbolsLeft = args[1]
                #Number of attempts left
            self.__GridSize = args[0]
                #Will be squared to make grid size
            self.__Grid = []
            for Count in range(1, self.__GridSize * self.__GridSize + 1):
                if random.randrange(1, 101) < 90:
                    #10% chance of getting > 90
                    C = Cell()
                        #90% chance of cell being empty
                else:
                    C = BlockedCell()
                        #10% chance of cell being blocked
                self.__Grid.append(C)
                    #Blank and blocked cells appended to the grid
            self.__AllowedPatterns = []
            self.__AllowedSymbols = []
                # Setting allowed patterns
            QPattern = Pattern("Q", "QQ**Q**QQ")
            """
                Instantiates a 'Pattern' Class
                The first parameter is the symbol.
                The second parameter is the way the symbol is placed onto the grid;
                    Matched onto the grid in a spiral pattern, starting at top left
                The asterisks represent any other symbol that may appear
            """
            self.__AllowedPatterns.append(QPattern)
            self.__AllowedSymbols.append("Q")
            XPattern = Pattern("X", "X*X*X*X*X")
            self.__AllowedPatterns.append(XPattern)
            self.__AllowedSymbols.append("X")
            TPattern = Pattern("T", "TTT**T**T")
            self.__AllowedPatterns.append(TPattern)
            self.__AllowedSymbols.append("T")

    def __LoadPuzzle(self, Filename):
        try:
            with open(Filename) as f:
                NoOfSymbols = int(f.readline().rstrip())#rstrip removes spaces in string
                #First line of text file contains number of symbols
                for Count in range (1, NoOfSymbols + 1):
                    """
                        Will iterate through the next 'NoOfSymbols' lines
                        These lines contain the symbols that are allowed
                    """
                    self.__AllowedSymbols.append(f.readline().rstrip())
                        #Allowed symbols set based on letters in text file
                NoOfPatterns = int(f.readline().rstrip())
                for Count in range(1, NoOfPatterns + 1):
                    Items = f.readline().rstrip().split(",")
                    P = Pattern(Items[0], Items[1])
                    self.__AllowedPatterns.append(P)
                        #Allowed patterns set based on allowed patterns in text files
                self.__GridSize = int(f.readline().rstrip())
                    #self.__GridSize = 5, as 5 is on next line to be read
                for Count in range (1, self.__GridSize * self.__GridSize + 1):
                    #Will loop through every space available in the grid
                    Items = f.readline().rstrip().split(",")
                    """
                        'Items' contains either 1 or 2 symbols, or a comma
                        Items[0] represents the symbol currently in a grid space
                        Items[1] represents symbols that can't be placed into a space
                    """
                    if Items[0] == "@":
                        C = BlockedCell()
                        self.__Grid.append(C)
                    else:
                        C = Cell()
                        C.ChangeSymbolInCell(Items[0])
                        
                        for CurrentSymbol in range(1, len(Items)):
                            #Iteration will start from Items[1]
                            C.AddToNotAllowedSymbols(Items[CurrentSymbol])
                        self.__Grid.append(C)
                self.__Score = int(f.readline().rstrip())
                    #2nd to last line contains current score
                self.__SymbolsLeft = int(f.readline().rstrip())
                    #Last line contains number of attempts left#
        except:
            print("Puzzle not loaded")

    def AttemptPuzzle(self):
        Finished = False
        while not Finished:
            RemoveSymbol = False
            self.DisplayPuzzle()
                #Create the grid
            print("Current score: " + str(self.__Score))
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            print(f"{self.__SymbolsLeft} symbols left.")
            AskRemove = input("Do you want to remove a symbol? Press enter to ignore: ")
            if len(AskRemove) != 0:
                RemoveSymbol = True 
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            Row = -1
                #Placeholder
            Valid = False
            while not Valid:
                try:
                    Row = int(input("Enter row number: "))
                    Valid = True
                except:
                    #Could be 'except ValueError:'
                    pass
            Column = -1
                #Placeholder
            Valid = False
            while not Valid:
                try:
                    Column = int(input("Enter column number: "))
                    Valid = True
                except:
                    pass
            CurrentCell = self.__GetCell(Row, Column)
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            if RemoveSymbol:
                if CurrentCell.IsEmpty():
                    print("Location is empty.")
                elif not CurrentCell.CheckSymbolAllowed(CurrentCell.GetSymbol()):
                    print("Cannot remove symbol from pre-existing pattern")
                elif CurrentCell.GetSymbol() == "@":
                    print("Blocked cells cannot be overwritten")
                else:
                    CurrentCell.ChangeSymbolInCell("")
                    self.__SymbolsLeft += 1
            #~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~#
            else:
                Symbol = self.__GetSymbolFromUser()
                    #Allows user to input symbols
                self.__SymbolsLeft -= 1
                    #Decrements number of attempts user has left
                if CurrentCell.CheckSymbolAllowed(Symbol):
                    CurrentCell.ChangeSymbolInCell(Symbol)
                    AmountToAddToScore = self.CheckforMatchWithPattern(Row, Column)
                    if AmountToAddToScore > 0:
                        self.__Score += AmountToAddToScore
                if self.__SymbolsLeft == 0:
                    Finished = True
        print()
        self.DisplayPuzzle()
        print()
        return self.__Score

    def __GetCell(self, Row, Column):
            #Returns the index of a cell
        Index = (self.__GridSize - Row) * self.__GridSize + Column - 1
            #This strange formula seems to be due to spiral method of placing items
        if Index >= 0:
            return self.__Grid[Index]
        else:
            raise IndexError()

    def CheckforMatchWithPattern(self, Row, Column):
        for StartRow in range(Row + 2, Row - 1, -1):
            for StartColumn in range(Column - 2, Column + 1):
                try:
                    PatternString = "" #Initially an empty string
                    #Goes through grid in spiral pattern to create string pattern
                    
                    PatternString += self.__GetCell(StartRow, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 2).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn + 1).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 2, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn).GetSymbol()
                    PatternString += self.__GetCell(StartRow - 1, StartColumn + 1).GetSymbol()
                    for P in self.__AllowedPatterns:
                        CurrentSymbol = self.__GetCell(Row, Column).GetSymbol()
                        if P.MatchesPattern(PatternString, CurrentSymbol):
                            self.__GetCell(StartRow, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 2).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 2, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn).AddToNotAllowedSymbols(CurrentSymbol)
                            self.__GetCell(StartRow - 1, StartColumn + 1).AddToNotAllowedSymbols(CurrentSymbol)
                            return 10
                            #10 points for completion of pattern
                except:
                    pass
        return 0

    def __GetSymbolFromUser(self):
        #Method to get user input and return it
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
        #Method creates a visual representation of grid
        print()
        if self.__GridSize < 10:
            print("  ", end='')
                #Changes end of line from '\n' to ' '
                #Essentially, will not print on new line
            for Count in range(1, self.__GridSize + 1):
                print(" " + str(Count), end='')
        print()
            #Adds empty line to separate
        print(self.__CreateHorizontalLine())
        for Count in range(0, len(self.__Grid)):
            if Count % self.__GridSize == 0 and self.__GridSize < 10:
                print(str(self.__GridSize - ((Count + 1) // self.__GridSize)) + " ", end='')
            print("|" + self.__Grid[Count].GetSymbol(), end='')
            if (Count + 1) % self.__GridSize == 0:
                print("|")
                print(self.__CreateHorizontalLine())

class Pattern():
    def __init__(self, SymbolToUse, PatternString):
        self.__Symbol = SymbolToUse
        self.__PatternSequence = PatternString

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

    def GetPatternSequence(self):
      return self.__PatternSequence

class Cell(): #PARENT CLASS OF "BlockedCell"
    def __init__(self):
        self._Symbol = ""
        self.__SymbolsNotAllowed = []

    def GetSymbol(self):
        if self.IsEmpty():
          return "-" #Represents an empty cell
        else:
          return self._Symbol #Q, X, T, or @
    
    def IsEmpty(self):
        #Checks if symbol is empty string - returns true if so
        if len(self._Symbol) == 0:
            #If self._Symbol is an empty string
            return True
        else:
            return False

    def ChangeSymbolInCell(self, NewSymbol):
        #Updates symbol; triggers for user input
        self._Symbol = NewSymbol

    def CheckSymbolAllowed(self, SymbolToCheck):
        print(self.__SymbolsNotAllowed)
        #Checks symbol against blocked symbols
        for Item in self.__SymbolsNotAllowed: 
            if Item == SymbolToCheck:
                return False
        return True

    def AddToNotAllowedSymbols(self, SymbolToAdd):
        #Add symbol to list of blocked symbols
        self.__SymbolsNotAllowed.append(SymbolToAdd)

    def UpdateCell(self):
        pass

class BlockedCell(Cell): #CHILD CLASS OF "Cell"
    def __init__(self):
        super(BlockedCell, self).__init__()
            #super__init__ method to inherit from Cell class' __init__ method
        self._Symbol = "@"

    def CheckSymbolAllowed(self, SymbolToCheck):
        #Will always return false since cell is always blocked
        return False

if __name__ == "__main__":
    Main()
