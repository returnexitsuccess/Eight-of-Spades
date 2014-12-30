# Eight of Spades v1.2

import math
import random
import os
import sys

class Game:
    def __init__(self, playinput):
        self.gameover = False
        self.numplayers = 0
        for numberof in playinput:
            self.numplayers += numberof
        
        self.players = []
        i = 0
        while (i < playinput[1]):
            self.players.append(naiveComputer(i + 1))
            i += 1

        while (i < playinput[1] + playinput[2]):
            self.players.append(Blake(i + 1))
            i += 1
        
        while (i < playinput[1] + playinput[2] + playinput[3]):
            self.players.append(Computer(i + 1))
            i += 1
        i = 0
        while (i < playinput[0]):
            self.players.append(Human(i + 1, self))
            if ("faris" in self.players[len(self.players) - 1].name.lower()):
                print "Andrew Faris is the worst"
            if ("george" in self.players[len(self.players) - 1].name.lower()):
                print "George, you can't play Eight of Spades with us"
                self.players.pop()

            i += 1
        # Initializing self.players

        for k in range(0, 100):
            for i in range(0, len(self.players)):
                j = random.randint(i, len(self.players) - 1)
                self.players[i], self.players[j] = self.players[j], self.players[i]
        # Shuffle Player Order

        self.board = Board()

        self.turn = 0

        self.debug = False
    def isOver(self):
        
        normalexists = False
        for i in range(0, 49):
            if (self.board.mask[i] == 0):
                normalexists = True
                break
        playerexists = False
        for player in self.players:
            if (player.points > 4):
                playerexists = True
                break
        if ((not normalexists) and (not playerexists)):
            return True
        # Checking if only the illuminati is left and if no one can play in the illuminati
        
        if (self.gameover):
            return True
        # Checking if someone won the game by picking the eight of spades in the illuminati or on the first turn

        if (len(self.players) == 0):
            return True
        
        for element in self.board.mask:
            if (element == 0):
                return False
        # Checking if any cards are left on the board

        return True
    def removePlayer(self):
        self.players.pop(self.turn % len(self.players))
    def end(self):
        if (not self.gameover):
            clear()
            self.board.display(self)
        print "GAME OVER"
        
        #for index in range(0, len(self.players)):
        #    print self.players[index].name + " has " + str(self.players[index].points) + " points"
            
class Player(object):
    def play(self, board, game):
        normalexists = False
        for i in range(0, 49):
            if (board.mask[i] == 0):
                normalexists = True
                break
        if (self.points < 5 and not normalexists):
            print self.name + " has no possible move"
            if (not game.debug):
                print "Press enter to proceed to the next turn..."
                raw_input()
            return 0
        # Checking to see if player has any possible moves
        
        card, guess = self.move(board, game)
        if (card == 0 or guess == 0):
            return 0
        # Calling individual player's move function and exiting if either is equal to 0

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
        # Printing what type of suit the card guessed was and the point value of the card
        
        if (guess == board.array[card - 1]): # If the guess was correct
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
            # Adding together all the points for the turn
            
            if (board.array[card - 1] == 5 and (card > 49 or game.turn < len(game.players))):
                game.gameover = True
                clear()
                board.display(game)
                print self.name + " wins"
                # Setting the win flag if the card is the Eight of Spades and the card was in the illuminati or it was their first turn
        elif (board.array[card - 1] == 6): # If the guess was the Ace of Spades
            print self.name + " has lost all their points"
            self.points = 0
            board.mask[card - 1] = 1
            if (card > 49):
                game.removePlayer()
                print self.name + " has been removed from the game"
                # Removing the player if they chose the Ace of Spades in the illuminati
        else: # If the guess was incorrect
            print self.name + "'s guess was incorrect"
            if (card < 50):
                board.mask[card - 1] = 1
            else:
                board.mask[card - 1] = 2
                self.points -= 5
        if (not game.debug):
            print "Press enter to proceed to the next turn..."
            raw_input()
        print "\n\n"
        return 0


class Human(Player):
    def __init__(self, number, game):
        self.type = "human"
        doesRepeat = True
        while (doesRepeat):
            doesRepeat = False
            while (True):
                self.name = "Player " + str(number)
                self.name = raw_input("Please set a name for " + self.name + "\n")
                if (self.name == "" or len(self.name) > 19):
                    print "That is not a valid name for this player, please select a new name"
                else:
                    break
            for player in game.players:
                if ((not (player is self)) and player.name == self.name):
                    print "That name is already taken, please select a new name for this player"
                    doesRepeat = True
                    break
                        
        self.points = 0
    def move(self, board, game):
        while (True):
            while (True):
                try:
                    card = int(raw_input(self.name + ", please select a card number:\n"))
                    break
                except ValueError:
                    pass
            if (board.mask[card - 1] != 0 or card <= 0 or card > 52):
                print "That is an invalid move"
            elif (card > 49 and self.points < 5):
                print "You do not have enough points to make that move"
            else:
                break
        print "1: Clubs\n2: Diamonds\n3: Hearts\n4: Spades\n5: Eight of Spades"

        append = ""
        if ("carmody" in self.name.lower()):
            append = "." * board.array[card - 1]
        
        while (True):
            while (True):
                try:
                    guess = int(raw_input("What do you think card number " + str(card) + " is" + append + "\n"))
                    break
                except ValueError:
                    pass
            if (guess < 1 or guess > 5):
                print "That is an invalid guess"
            else:
                break
        return card, guess
       

class Computer(Player):
    def __init__(self, number):
        self.type = "hard"
        self.name = "Computer " + str(number) + " (H)"
        print self.name + " has been created"
        self.points = 0
    def ai(self, board, game):
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
            if (board.mask[index]):
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
            if (board.mask[index] == 1):
                pot += 1
            elif (board.mask[index] == 3):
                a = board.array[index]
                if (a == 5 or a == 6):
                    a = 4
                locked[a - 1] += 1

        totalpoints = 0
        for player in game.players:
            totalpoints += player.points

        normal = [0, 0, 0, 0, 0]
        ''' normal = [clubs, diamonds, hearts, spades, eight]'''
        normal[4] = (locked[3] + pot + int(math.ceil(52.0 / len(game.players)))) * ((1.0 - eightdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        normal[0] = (locked[0] + pot + 1) * ((13.0 - clubsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        normal[1] = (locked[1] + pot + 1) * ((13.0 - diamondsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        normal[2] = (locked[2] + pot + 1) * ((13.0 - heartsdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        normal[3] = (locked[3] + pot + 1) * ((11.0 - spadesdrawn) / (52 - cardsdrawn)) - (self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))

        illuminati = [0, 0, 0, 0, 0]
        illuminati[4] = ((int(math.ceil((77.0 + int(math.ceil(52.0 / len(game.players)))) / len(game.players)))) - self.points) * ((1.0 - eightdrawn) / (52 - cardsdrawn)) - (5) * ((50 - cardsdrawn) / (52 - cardsdrawn)) - (77 + int(math.ceil(52.0 / len(game.players))) - totalpoints + self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        illuminati[0] = (locked[0] + pot + 10) * ((13.0 - clubsdrawn) / (52 - cardsdrawn)) - (5) * ((39.0 - cardsdrawn + clubsdrawn) / (52 - cardsdrawn)) - (77 + int(math.ceil(52.0 / len(game.players))) - totalpoints + self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        illuminati[1] = (locked[1] + pot + 10) * ((13.0 - diamondsdrawn) / (52 - cardsdrawn)) - (5) * ((39.0 - cardsdrawn + diamondsdrawn) / (52 - cardsdrawn)) - (77 + int(math.ceil(52.0 / len(game.players))) - totalpoints + self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        illuminati[2] = (locked[2] + pot + 10) * ((13.0 - heartsdrawn) / (52 - cardsdrawn)) - (5) * ((39.0 - cardsdrawn + heartsdrawn) / (52 - cardsdrawn)) - (77 + int(math.ceil(52.0 / len(game.players))) - totalpoints + self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))
        illuminati[3] = (locked[3] + pot + 10) * ((11.0 - spadesdrawn) / (52 - cardsdrawn)) - (5) * ((41.0 - cardsdrawn + spadesdrawn) / (52 - cardsdrawn)) - (77 + int(math.ceil(52.0 / len(game.players))) - totalpoints + self.points) * ((1.0 - acedrawn) / (52 - cardsdrawn))

        return normal, illuminati
    def move(self, board, game):
        normal, illuminati = self.ai(board, game)
        highestn = normal[0]
        indexn = 0
        highesti = illuminati[0]
        indexi = 0
        for i in range(1, 5):
            if (normal[i] > highestn):
                indexn = i
                highestn = normal[i]
            if (illuminati[i] > highesti and self.points > 4):
                indexi = i
                highesti = illuminati[i]
        
        normalexists = False
        for i in range(0, 49):
            if (board.mask[i] == 0):
                normalexists = True
                break

        illuminatiexists = False
        for i in range(49, 52):
            if (board.mask[i] == 0):
                illuminatiexists = True
                break
        '''
        if (not normalexists):
            highestn = 0
        elif (not illuminatiexists):
            highesti = 0
        '''
        
        if ((highesti >= highestn or (not normalexists)) and self.points > 4 and illuminatiexists):
            card = random.randint(50, 52)
            while (board.mask[card - 1] != 0):
                card = random.randint(50, 52)
            guess = indexi + 1
            if (indexi == 0):
                fill = "Clubs"
            elif (indexi == 1):
                fill = "Diamonds"
            elif (indexi == 2):
                fill = "Hearts"
            elif (indexi == 3):
                fill = "Spades"
            elif (indexi == 4):
                fill = "the Eight of Spades"
        else:
            card = random.randint(1, 49)
            while (board.mask[card - 1] != 0):
                card = random.randint(1, 49)
            guess = indexn + 1
            if (indexn == 0):
                fill = "Clubs"
            elif (indexn == 1):
                fill = "Diamonds"
            elif (indexn == 2):
                fill = "Hearts"
            elif (indexn == 3):
                fill = "Spades"
            elif (indexn == 4):
                fill = "the Eight of Spades"
        # print self.name + " has " + str(self.points) + " points"
        print self.name + " guessed " + fill + " on card number " + str(card)
        return card, guess
            
class naiveComputer(Player):
    illuminati = random.randint(25, 40)
    eightofspades = random.randint(30, 45)
    def __init__(self, number):
        self.type = "easy"
        self.name = "Computer " + str(number) + " (E)"
        print self.name + " has been created"
        self.points = 0
    def move(self, board, game):
        
        normalexists = False
        for i in range(0, 49):
            if (board.mask[i] == 0):
                normalexists = True
                break

        illuminatiexists = False
        for i in range(49, 52):
            if (board.mask[i] == 0):
                illuminatiexists = True
                break
        
        if (self.points > 4 and (self.illuminati > random.randint(0, 99) or not normalexists) and illuminatiexists):
            card = random.randint(50, 52)
            while (board.mask[card - 1] != 0):
                card = random.randint(50, 52)
        else:
            card = random.randint(1, 49)
            while (board.mask[card - 1] != 0):
                card = random.randint(1, 49)

        if (self.eightofspades > random.randint(0, 99)):
            guess = 5
            fill = "the Eight of Spades"
        else:
            guess = random.randint(1, 4)

        if (guess == 1):
            fill = "Clubs"
        elif (guess == 2):
            fill = "Diamonds"
        elif (guess == 3):
            fill = "Hearts"
        elif (guess == 4):
            fill = "Spades"

        print self.name + " guessed " + fill + " on card number " + str(card)

        return card, guess

class Blake(naiveComputer):
    def __init__(self, number):
        self.type = "medium"
        self.name = "Computer " + str(number) + " (M)"
        print self.name + " has been created"
        self.points = 0
    def blakeRules(self, board, game):
        cardsflipped = 0
        cardsleft = 52
        eightdrawn = 0
        for i in range(0, 52):
            if (board.mask[i] == 1):
                cardsflipped += 1
            if (board.mask[i] != 0):
                cardsleft -= 1
                if (board.array[i] == 5):
                    eightdrawn = 1

        if (cardsflipped == 0):
            self.eightofspades = 99
        elif (cardsflipped == 1):
            self.eightofspades = 75
        elif (cardsflipped == 2):
            self.eightofspades = 50
        elif (cardsflipped == 3):
            self.eightofspades = 25
        else:
            self.eightofspades = 5

        if (cardsleft < 26):
            self.eightofspades *= 2
        if (cardsleft < len(game.players)):
            self.illuminati = 100
            for player in game.players:
                if (player.points - self.points > 9):
                    self.eightofspades = 100
                    break
        if (eightdrawn == 1):
            self.eightofspades = 0

    def move(self, board, game):
        self.blakeRules(board, game)
        return super(Blake, self).move(board, game)
        


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
        print ""
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
                    

def clear():
    if (not ("idlelib.run" in sys.modules)):
        if (sys.platform == "win32"):
            os.system('cls') # Windows
        elif (sys.platform == "darwin"):
            os.system('clear') # Unix (Mac OS X and Linux)

def main():

    if (not ("idlelib.run" in sys.modules)):
        os.system("mode con: cols=80 lines=45")

        os.environ['LINES'] = "45"
        os.environ['COLUMNS'] = "80"


    DEBUG_MODE = False
    while (True):
        try:
           with open('debug.txt'): pass
        except IOError:
           break
        answer = raw_input("Would you like to enter debug mode? (y/n)\n")
        if (answer == "y"):
            DEBUG_MODE = True
        break

    '''
    osversion = ""
    while (osversion != "1" and osversion != "2"):
        print "Please select your OS:\n1: Windows\n2: Mac/Linux"
        osversion = raw_input()
    

    if (sys.platform == "win32"):
        print "OS is Windows"
        osversion = "1"
    elif (sys.platform == "darwin"):
        print "OS is Mac"
        osversion = "2"
    '''


    while (True):
        answer = ""
        playinput = [0, 0, 0, 0]
        # playinput = [human, easy, medium, hard]
        while (True):
            while (True):
                try:
                    playinput[0] = int(raw_input("How many human players:\n"))
                    if (playinput[0] >= 0):
                        break
                except ValueError:
                    pass
            while (True):
                try:
                    playinput[1] = int(raw_input("How many easy computer players:\n"))
                    if (playinput[1] >= 0):
                        break
                except ValueError:
                    pass
            while (True):
                try:
                    playinput[2] = int(raw_input("How many medium computer players:\n"))
                    if (playinput[2] >= 0):
                        break
                except ValueError:
                    pass
            while (True):
                try:
                    playinput[3] = int(raw_input("How many hard computer players:\n"))
                    if (playinput[3] >= 0):
                        break
                except ValueError:
                    pass
            if (sum(playinput) < 20):
                break
            else:
                clear()
                print "There are too many players, please choose less than 20"
        game = Game(playinput)
        game.debug = DEBUG_MODE
        while (not game.isOver()):
            clear()
            game.board.display(game)
            game.players[game.turn % len(game.players)].play(game.board, game)
            game.board.checkLock()
            game.turn += 1
        game.end()
        while (answer != "y" and answer != "n"):
            print "\nThe End is the Beginning\nDo you want to play again: y/n?"
            answer = raw_input()
        if (answer == "n"):
            break
        clear()
        
main()
