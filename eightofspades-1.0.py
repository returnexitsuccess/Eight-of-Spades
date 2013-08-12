import math
import random
import os
import sys

class Game:
    def __init__(self, human, computer):
        self.numplayers = human + computer
        
        self.players = []

        i = 0
        while (i < human):
            self.players.append(Human(i + 1))
            i += 1

        i = 0
        while (i < computer):
            self.players.append(Computer(i + 1))
            i += 1

        self.board = Board()

        self.turn = 0
    def isOver(self):
        global gameover
        if (gameover):
            return False
        for element in self.board.mask:
            if (element == 0):
                return False
        return True
    def removePlayer(self):
        self.players.pop(turn)
    def end(self):
        global gameover
        if (not gameover):
            clear()
            self.board.display(self)
        print "GAME OVER"
        
        #for index in range(0, len(self.players)):
        #    print self.players[index].name + " has " + str(self.players[index].points) + " points"
            

class Human:
    def __init__(self, number):
        self.name = "Player " + str(number)
        print "Please set a name for " + self.name
        self.name = raw_input()
        self.points = 0
    def play(self, board, game):
        # print self.name + " has " + str(self.points) + " points"
        print self.name + ", please select a card number:"
        card = int(raw_input())
        if (board.mask[card - 1] != 0 or card <= 0 or card > 52):
            print "That is an invalid move, your turn has been skipped"
            return 1
        if (card > 49 and self.points < 5):
            print "You do not have enough points to make that move"
            print "Your turn has been skipped"
            return 2
        print "1: Clubs\n2: Diamonds\n3: Hearts\n4: Spades\n5: Eight of Spades"
        print "What do you think card number " + str(card) + " is?"
        guess = int(raw_input())
        if (guess < 1 or guess > 5):
            print "That is an invalid guess, your turn has been skipped"
            return 3
        point = 1
        if (board.array[card - 1] == 1):
            suit = "Clubs"
        elif (board.array[card - 1] == 2):
            suit = "Diamonds"
        elif (board.array[card - 1] == 3):
            suit = "Hearts"
        elif (board.array[card - 1] == 4):
            suit = "Spades"
        elif (board.array[card - 1] == 5):
            suit = "Eight of Spades"
            point = int(math.ceil(52.0 / len(game.players)))
        elif (board.array[card - 1] == 6):
            suit = "Ace of Spades"
        print str(card) + " is " + suit
        if (card > 49):
            point *= 10
        if (guess == board.array[card - 1]):
            print "Your guess was correct"
            board.mask[card - 1] = 2
            self.points += point
            for index in range(0, len(board.mask)):
                if (board.mask[index] == 1):
                    board.mask[index] = 2
                    self.points += 1
                elif (board.mask[index] == 3):
                    if (board.array[index] == guess):
                        board.mask[index] = 2
                        self.points += 1
                    elif (guess > 3 and board.array[index] > 3):
                        board.mask[index] = 2
                        self.points += 1
            if (card > 49 and board.array[card - 1] == 5):
                global gameover
                gameover = True
                clear()
                board.display(game)
                print self.name + " wins"
        elif (board.array[card - 1] == 6):
            print "You have lost all your points"
            self.points = 0
            board.mask[card - 1] = 1
            if (card > 49):
                game.removePlayer()
                print "You have been removed from the game"
        else:
            print "Your guess was incorrect"
            if (card < 50):
                board.mask[card - 1] = 1
            else:
                board.mask[card - 1] = 2
                self.points -= 5
        print "Press enter to proceed to the next turn..."
        raw_input()
        return 0
            
        

class Computer:
    def __init__(self, number):
        self.name = "Computer " + str(number)
        print self.name + " has been created"
        self.points = 0
    def play(self, board, game):
        pot = 0
        clubsdrawn = 0
        diamondsdrawn = 0
        heartsdrawn = 0
        spadesdrawn = 0
        eightdrawn = 0
        acedrawn = 0
        cardsdrawn = 0
        locked = [0, 0, 0, 0]
        for index in range(0, 52):
            if (board.mask[index] == 1):
                pot += 1
            elif (board.mask[index] == 2):
                a = board.array[index]
                cardsdrawn += 1
                if (a == 1):
                    clubsdrawn += 1
                elif (a == 2):
                    diamondsdrawn += 1
                elif (a == 3):
                    heartsdrawn += 1
                elif (a == 4):
                    spadesdrawn += 1
                elif (a == 5):
                    eightdrawn += 1
                elif (a == 6):
                    acedrawn += 1
            elif (board.mask[index] == 3):
                a = board.array[index]
                if (a == 5 or a == 6):
                    a = 4
                locked[a - 1] += 1
        eight = (locked[3] + pot + int(math.ceil(52.0 / len(game.players)))) * ((1.0 - eightdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        clubs = (locked[0] + pot + 1) * ((13.0 - clubsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        diamonds = (locked[1] + pot + 1) * ((13.0 - diamondsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        hearts = (locked[2] + pot + 1) * ((13.0 - heartsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        spades = (locked[3] + pot + 1) * ((12.0 - spadesdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        highest = max(eight, clubs, diamonds, hearts, spades)
        if (eight == highest):
            guess = 5
            fill = "the Eight of Spades"
        elif (clubs == highest):
            guess = 1
            fill = "Clubs"
        elif (diamonds == highest):
            guess = 2
            fill = "Diamonds"
        elif (hearts == highest):
            guess = 3
            fill = "Hearts"
        elif (spades == highest):
            guess = 4
            fill = "Spades"

        card = random.randint(1, 49)
        i = 0
        while (board.mask[card - 1] != 0):
            if ((i + 1) % 100 != 0):
                card = random.randint(1, 49)
            elif (self.points > 4):
                card = random.randint(50, 52)
            i += 1
        # print self.name + " has " + str(self.points) + " points"
        print self.name + " guessed " + fill + " on card number " + str(card)
        point = 1
        if (board.array[card - 1] == 1):
            suit = "Clubs"
        elif (board.array[card - 1] == 2):
            suit = "Diamonds"
        elif (board.array[card - 1] == 3):
            suit = "Hearts"
        elif (board.array[card - 1] == 4):
            suit = "Spades"
        elif (board.array[card - 1] == 5):
            suit = "Eight of Spades"
            point = int(math.ceil(52.0 / len(game.players)))
        elif (board.array[card - 1] == 6):
            suit = "Ace of Spades"
        print str(card) + " is " + suit
        if (card > 49):
            point *= 10
        if (guess == board.array[card - 1]):
            print self.name + "'s guess was correct"
            board.mask[card - 1] = 2
            self.points += point
            for index in range(0, len(board.mask)):
                if (board.mask[index] == 1):
                    board.mask[index] = 2
                    self.points += 1
                elif (board.mask[index] == 3):
                    if (board.array[index] == guess):
                        board.mask[index] = 2
                        self.points += 1
                    elif (guess > 3 and board.array[index] > 3):
                        board.mask[index] = 2
                        self.points += 1
            if (card > 49 and board.array[card - 1] == 5):
                global gameover
                gameover = True
                clear()
                board.display(game)
                print self.name + " wins"
        elif (board.array[card - 1] == 6):
            print self.name + " has lost all their points"
            self.points = 0
            board.mask[card - 1] = 1
            if (card > 49):
                game.removePlayer()
                print self.name + " has been removed from the game"
        else:
            print self.name + "'s guess was incorrect"
            if (card < 50):
                board.mask[card - 1] = 1
            else:
                board.mask[card - 1] = 2
                self.points -= 5
        print "Press enter to proceed to the next turn..."
        raw_input()
        return 0

        
            

class Board:
    def __init__(self):
        self.array = []
        # 1 is clubs
        # 2 is diamonds
        # 3 is hearts
        # 4 is spades
        # 5 is eight of spades
        # 6 is ace of spades
        for i in range(0, 13):
            self.array.append(1)
        for i in range(0, 13):
            self.array.append(2)
        for i in range(0, 13):
            self.array.append(3)
        for i in range(0, 11):
            self.array.append(4)
        self.array.append(5)
        self.array.append(6)
        # Create Array

        for k in range(0, 100):
            for i in range(0, 52):
                j = random.randint(i, 51)
                self.array[i], self.array[j] = self.array[j], self.array[i]
        # Shuffle Array 100 times

        self.mask = []
        # 0 is unflipped
        # 1 is flipped
        # 2 is taken
        # 3 is locked
        for i in range(0, 52):
            self.mask.append(0)
        # Create Mask
    def display(self, game):
        '''
        global osversion
        if (osversion == "1"):
            os.system('cls') # Windows
        elif (osversion == "2"):
            os.system('clear') # Unix (Mac OS X and Linux)
        '''

        '''
        for player in game.players:
            print player.name + " has " + str(player.points) + " points"
        '''
        
        print "* * * * * * * * * * * * * * * * *"
        for row in range(0, 7):
            print "*" + (" " * 31) + "*"
            line = "*  "
            for column in range(0, 7):
                current = row * 7 + column
                if (self.array[current] == 1):
                    char = "c"
                elif (self.array[current] == 2):
                    char = "d"
                elif (self.array[current] == 3):
                    char = "h"
                elif (self.array[current] > 3):
                    char = "s"
                if (self.mask[current] == 3):
                    char = char + "*"
                else:
                    char = char + " "
                spaces = "   "
                if (current >= 9):
                    spaces = "  "
                if (self.mask[current] == 0):
                    line = line + str(current + 1) + spaces
                elif (self.mask[current] == 1 or self.mask[current] == 3):
                    line = line + char + "  "
                elif (self.mask[current] == 2):
                    line = line + "    "
            line = line + " *"
            print line
        print "*                               *"
        line = "*   "
        for i in range(49, 52):
            if (self.array[i] == 1):
                char = "c"
            elif (self.array[i] == 2):
                char = "d"
            elif (self.array[i] == 3):
                char = "h"
            elif (self.array[i] > 3):
                char = "s"
            if (self.mask[current] == 3):
                char = char + "*"
            else:
                char = char + " "
            if (self.mask[i] == 0):
                line = line + "   " + str(i + 1) + "   "
            elif (self.mask[i] == 1 or self.mask[i] == 3):
                line = line + "   " + char + "   "
            elif (self.mask[i] == 2):
                line = line + "   " + "  " + "   "
        line = line + "    *"
        print line
        print "*" + (" " * 31) + "*"
        print "* * * * * * * * * * * * * * * * *"
        for player in game.players:
            print player.name + " has " + str(player.points) + " points"
    def checkLock(self):
        for index in range(0, 49):
            if (self.mask[index] == 1 or self.mask[index] == 3):
                if ((index + 1) % 7 != 0):
                    if (self.mask[index + 1] == 1 or self.mask[index + 1] == 3):
                        if (self.array[index] == self.array[index + 1] or self.array[index] > 3 and self.array[index + 1] > 3):
                            self.mask[index] = 3
                            self.mask[index + 1] = 3
                if (index < 42):
                    if (self.mask[index + 7] == 1 or self.mask[index + 7] == 3):
                        if (self.array[index] == self.array[index + 7] or self.array[index] > 3 and self.array[index + 7] > 3):
                            self.mask[index] = 3
                            self.mask[index + 7] = 3
                    
                    

os.system("mode con: cols=80 lines=45")

os.environ['LINES'] = "45"
os.environ['COLUMNS'] = "80"

'''
osversion = ""
while (osversion != "1" and osversion != "2"):
    print "Please select your OS:\n1: Windows\n2: Mac/Linux"
    osversion = raw_input()
'''

if (sys.platform == "win32"):
    print "OS is Windows"
    osversion = "1"
elif (sys.platform == "darwin"):
    print "OS is Mac"
    osversion = "2"

def clear():
    if (osversion == "1"):
        os.system('cls') # Windows
    elif (osversion == "2"):
        os.system('clear') # Unix (Mac OS X and Linux)

playagain = True
while (playagain):
    answer = ""
    gameover = False
    print "How many human players:"
    human = int(raw_input())
    print "How many computer players:"
    computer = int(raw_input())
    game = Game(human, computer)
    while (not game.isOver()):
        clear()
        game.board.display(game)
        game.players[game.turn % len(game.players)].play(game.board, game)
        game.board.checkLock()
        game.turn += 1
    game.end()
    while (answer != "y" and answer != "n"):
        print "\nDo you want to play again: y/n?"
        answer = raw_input()
    if (answer == "n"):
        playagain = False
    clear()
    
