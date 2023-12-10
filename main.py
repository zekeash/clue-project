import random

#gameplay:
# put players in starting locations
# select envelope and deal out cards
# create + update each player's notebooks
# turn taking
# a player's turn:
#    chance to move
#    suggest/accuse/skip (if in a room)
#    if suggest:
#       collect a response and update notebook
#    if accuse:
#       check middle

## public log

# player who asked what -> player who responded, if anyone. players who didn't respond.

## private log

# the notebook
# what you've shown

class Board:

    def __init__(self):
        #self.playerOrder = players in game (start w miss scarlet)

    def showBoard(self):


class Player:

    def __init__(self, name, location):
        self.name = name
        self.location = location
        #self.notebook = self.createNotebook()
        #self.hand = random cards from deck

    def createNotebook(self, deck, game):
        notebook = {}
        for card in deck:
            for player in game:
                notebook[card][player] = " "
        return notebook

    def updateNotebook(self):
        ...

    def getInfo(self):
        ...

    def getHand(self):
        ...

    def move(self):
        ...

    def playerTurn(self):
        # need to include something about moving
        # after entering a new location:
        if input("would you like to make a suggestion (type 'yes' if so)?") == "yes" or "Yes":
            suspect = input("which character would you like to suggest?")
            weapon = input("what weapon did they use?")
            # case insensitive
            suggestion = suggest(suspect, self.location, weapon)
            self.gatherResponses(suggestion, playerList)
            # has someone responded? == False
            # for player in list (if HSR? == False)
                # chance to respond
                # if response, HSR? == True
        # if no offer to accuse

    def suggest(self,player,room,weapon):
        return [player,room,weapon]

    def gatherResponses(self,suggestion, players):
        for player in players:
            options = [card in player.hand if card in suggestion]
        # if player not human, random.choice(options) (or something smarter)
        if len(options) > 1:
            print(f"you have {options}. which card would you like to show active player")
            # advise player they have previously shown {read from log}.
            #allow for a choice if you have 2 or more of the suggestion
            #report and write to log
        elif len(options) == 1:
            # show card
            return options[0]
        else:
            print("you do not have the requested info")
        ...

    def accuse(self,suggestion):
        if suggestion == envelope:
            print("you win!")
        else:
            print("you guessed wrong! you are king of lose mountain")

class Deck:

    def __init__(self):
        self.playercards = ["Miss Scarlet", "Colonel Mustard", "Mr. Green", "Mrs. Peacock", "Prof. Plum", "Mrs. White"]
        self.roomcards = ["Study", "Kitchen", "Ballroom", "Conservatory", "Billiard Room",
                          "Library", "Hall", "Lounge", "Dining Room"]
        self.weaponcards = ["Candlestick", "Dagger", "Revolver", "Lead pipe", "Wrench", "Rope"]
        self.fresh_deck = self.playercards + self.roomcards + self.weaponcards
        self.deck = self.playercards + self.roomcards + self.weaponcards
        print(self.deck)
        #self.

    def prepPerp(self, player,room,weapon):
        #select a room, weapon, and character as the culprits and remove them from the deck
        self.deck.remove(player)
        self.deck.remove(room)
        self.deck.remove(weapon)
        return [player,room,weapon]

    def dealCards(self,numPlayers):
        for i in range(len(self.deck)//numPlayers):
            # player.hand = sel
        ...

deck = Deck()
envelope = deck.prepPerp(random.choice(deck.playercards),random.choice(deck.roomcards),random.choice(deck.weaponcards))
print(envelope)

class Place:

    # constructor
    def __init__(self, name):
        self.name = name
        self.paths = {}
        self.beings = []
        self.unownedThings = []

    def __str__(self):
        return self.name

    # displays the Place's internal information
    def info(self):
        print(f"Place name: {self.name}")
        print("Paths from here:")
        for direction in self.paths:
            otherPlace = self.paths[direction]
            print(f"  {direction} to {otherPlace}")

    def connectOneWay(self, direction, destination):
        if direction in self.paths:
            print(f"Error: a path {direction} from {self} already exists")
        else:
            self.paths[direction] = destination

    def connect(self, direction, destination):
        self.connectOneWay(direction, destination)
        opposite = {'up': 'down', 'down': 'up', 'north': 'south',
                    'south': 'north', 'east': 'west', 'west': 'east'}
        destination.connectOneWay(opposite[direction], self)

scarletStart = Place("Miss Scarlet Start")
mustardStart = Place("Colonel Mustard Start")
greenStart = Place("Mr. Green Start")
peacockStart = Place("Mrs. Peacock Start")
plumStart = Place("Professor Plum Start")
whiteStart = Place("Mrs. White Start")

study = Place("Study")
kitchen = Place("Kitchen")
ballroom = Place("Ballroom")
conservatory = Place("Conservatory")
billiardRoom = Place("Billiard Room")
library = Place("Library")
hall = Place("Hall")
lounge = Place("Lounge")
diningRoom = Place("Dining Room")

corridor1 = Place("Corridor")
corridor2 = Place("Corridor")
corridor3 = Place("Corridor")
corridor4 = Place("Corridor")


#initialize notebook:
notebook = {}
for card in deck.fresh_deck:
    notebook[card] = {}
    for player in deck.playercards:
        notebook[card][player] = ''

        
notebook['Rope']['Miss Scarlet'] = 'x'
notebook['Colonel Mustard']['Miss Scarlet'] = 'x'
notebook['Colonel Mustard']['Mr. Green'] = 'o'
notebook['Mr. Green']['Colonel Mustard']
notebook['Colonel Mustard']['Miss Scarlet'] 
notebook['Colonel Mustard']['Mr. Green']
notebook


notebook['Colonel Mustard']['Miss Scarlet'] = 'o'
notebook['Colonel Mustard']['Mr. Green'] = 'o'
notebook['Colonel Mustard']['Colonel Mustard'] = 'o'
notebook['Colonel Mustard']['Prof. Plum'] = 'o'
notebook['Colonel Mustard']['Mrs. White'] = 'o'
notebook['Colonel Mustard']['Mrs. Peacock'] = 'o'


def ready_to_accuse():
    no_one = {}
    for card in deck.fresh_deck:
        no_one[card]=0
        for player in deck.playercards:
            if notebook[card][player] == 'o':
                no_one[card] = no_one[card] + 1
        if no_one[card] == 6:
            print(card)


        
#for card in deck:
#   for player in game:
#       notebook[card][player] = "x" or "o" depending
# return notebook


# how your notebook should look:

##  suspects:     me    p1      p2      p3
##  Scarlet       x     o       o       o
##  Mustard       o     o       x       o
##  Plum          o     o       x       o

##  weapons:
##  Lead Pipe     o     o       o       o
##  Wrench        o     x       o       o
##  Candlestick   o     o       o       o
