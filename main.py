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

## jim suggests maybe making a setup or test command
public_log = []

# player who asked what -> player who responded, if anyone. players who didn't respond.
gameOver = True


def main():
    # setup goes here
    #playerOrder = playerList
    gameOver = False
    # enter some rules

    #beginning of the turn
    while gameOver == False:
        for player in playerList:
            player.playerTurn()
            for player in playerList:
                print(player.name)

## private log

# the notebook
# what you've shown

#class Board:

#    def __init__(self):
#        self.rooms =
        #self.playerOrder = players in game (start w miss scarlet)

 #   def showBoard(self):
 #       ...


class Player:

    def __init__(self, name, location):
        self.name = name
        self.location = location
        self.location.players.append(self)
        self.notebook = self.createNotebook(deck)
        self.hand = []

    def __str__(self):
        return self.name

    def createNotebook(self, deck):
        notebook = {}
        for card in deck.fresh_deck:
            notebook[card] = {}
            for player in deck.playercards:
                notebook[card][player] = ''
        return notebook

    def displayNotebook(self):
        for card in deck.fresh_deck:
            print(card, self.notebook[card])

    def updateNotebook(self,card,player,symbol):
        self.notebook[card][player] = symbol
        return self.notebook

    def getInfo(self):
        return f"I am {self.name}. I am currently in {self.location}."

    def getHand(self):
        ...

    def moveTo(self, newLocation):
        self.location.players.remove(self)
        newLocation.players.append(self)
        self.location = newLocation

    def go(self, direction):
        if direction not in self.location.paths:
            print(f"I don't see how to go {direction} from here.")
        else:
            destination = self.location.paths[direction]
            #if not destination.accepts(self):
            #    print(f"I'm not allowed to go to {destination}")
            #else:
            print(f"{self} moves from {self.location} to {destination}")
            self.moveTo(destination)

    def suggest(self,player,room,weapon):
        return [player,room,weapon]

    def playerTurn(self):
        # need to include something about moving
        # after entering a new location:
        # tell player possible moves and current location
        print(f"""It is your turn, {self.name}! 
You are in {self.location}!""")
        for direction in self.location.paths:
            otherPlace = self.location.paths[direction]
            print(f"  {direction} to {otherPlace}")
        move = input("which direction would you like to move?")
        self.go(move)
        # check if you are in a room where you can suggest/accuse
        if input("would you like to make a suggestion (type 'yes' if so)?") == "yes" or "Yes":
            suspect = input("which character would you like to suggest (simply type the color)?")
            suspect_object = get_object_by_name(suspect)
            suspect_object.moveTo(self.location)
            print(f"{suspect_object} has been called to the {self.location}")
            # move suspect to location
            weapon = input("what weapon did they use?")
            # case insensitive
            otherPlayers = playerList
            otherPlayers.remove(self)
            self.gatherResponses([suspect_object.name, self.location.name, weapon], otherPlayers)
            # has someone responded? == False
            # for player in list (if HSR? == False)
                # chance to respond
                # if response, HSR? == True
        # if no offer to accuse

    def gatherResponses(self, suggestion, players):
        for player in players:
            options = []
            for card in player.hand:
                if card in suggestion:
                    options.append(card)
        # if player not human, random.choice(options) (or something smarter)
            if len(options) > 1:
                cue = input(f"{player}, you have some of the suggested cards. Press any key to choose one to show.")
                print(options)
                shownCard = input(f"""{self.name} suggested {suggestion}. You have {options}.
Which card would you like to show {self.name}?""")
                self.updateNotebook(shownCard, player.name, "x")
                print(f"{player} shows the card {options[0]}.")
                public_log.append(f"""{self.name} suggested, {suggestion}.
{player.name} showed something""")
                return shownCard
            elif len(options) == 1:
                print(f"{player} shows the card {options[0]}.")
                self.updateNotebook(options[0],player.name,"x")
                public_log.append(f"""{self.name} suggested, {suggestion}.
{player.name} showed something""")
                return options[0]
            else:
                print
                print(f"{player} does not have the requested info")
        public_log.append(f"""{self.name} suggested, {suggestion}.
        Nobody knew nuthin'.""")

    def ready_to_accuse(self):
        no_one = {}
        for card in deck.fresh_deck:
            no_one[card] = 0
            for player in deck.playercards:
                if player.notebook[card][player] == 'o':
                    no_one[card] = no_one[card] + 1
            if no_one[card] == 6:
                print(card)

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
        #print(self.deck)
        #self.

    def prepPerp(self, player,room,weapon):
        #select a room, weapon, and character as the culprits and remove them from the deck
        self.deck.remove(player)
        self.deck.remove(room)
        self.deck.remove(weapon)
        return [player,room,weapon]

#    def dealCards(self,numPlayers):
#        for i in range(len(self.deck)//numPlayers):
            # player.hand = sel
#        ...

class Place:

    # constructor
    def __init__(self, name):
        self.name = name
        self.paths = {}
        self.players = []

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


deck = Deck()
envelope = deck.prepPerp(random.choice(deck.playercards),random.choice(deck.roomcards),random.choice(deck.weaponcards))
print(envelope)

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

scarlet = Player("Miss Scarlet", corridor1)
peacock = Player("Miss Peacock", corridor2)
mustard = Player("Colonel Mustard", corridor3)
green = Player("Mr. Green", corridor3)
white = Player("Mrs. White", corridor4)
plum = Player("Prof. Plum", corridor1)

playerList = {scarlet,peacock,plum,mustard,green,white}

# dealing cards:

for player in playerList:
    for r in range(3):
        card = random.choice(deck.deck)
        player.hand.append(card)
        deck.deck.remove(card)
    print(f"{player}'s hand: {player.hand}")
    for card in player.hand:
        player.updateNotebook(card,player.name,"x")


#initialize notebook:

def get_object_by_name(object_name):
    # Use globals() or locals() to access the global or local namespace
    # In this example, we'll use globals()
    global_namespace = globals()

    # Check if the object with the given name exists in the global namespace
    if object_name in global_namespace:
        return global_namespace[object_name]
    else:
        return None

#object_name_input = input("Enter the name of the object: ")
#result_object = get_object_by_name(object_name_input)
#print(result_object)
#print(result_object.location)
        
#plum.notebook['Rope']['Miss Scarlet'] = 'x'
#plum.notebook['Colonel Mustard']['Miss Scarlet'] = 'x'
#plum.notebook['Colonel Mustard']['Mr. Green'] = 'o'
#plum.notebook['Mr. Green']['Colonel Mustard']
#plum.notebook['Colonel Mustard']['Miss Scarlet']
#plum.notebook['Colonel Mustard']['Mr. Green']



#plum.notebook['Colonel Mustard']['Miss Scarlet'] = 'o'
#plum.notebook['Colonel Mustard']['Mr. Green'] = 'o'
#plum.notebook['Colonel Mustard']['Colonel Mustard'] = 'o'
#plum.notebook['Colonel Mustard']['Prof. Plum'] = 'o'
#plum.notebook['Colonel Mustard']['Mrs. White'] = 'o'
#plum.notebook['Colonel Mustard']['Mrs. Peacock'] = 'o'
#plum.displayNotebook()


        
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

# connecting the board

corridor1.connect("south", corridor2)
corridor2.connect("south", corridor3)
corridor3.connect("south", corridor4)

corridor1.connect("east", lounge)
corridor1.connect("west", study)

corridor2.connect("east", library)
corridor2.connect("west", diningRoom)

corridor3.connect("east", ballroom)
corridor3.connect("west", billiardRoom)

corridor4.connect("east", kitchen)
corridor4.connect("west", conservatory)

#lounge.connect("secret passage", conservatory)
#study.connect("secret passage", kitchen)
