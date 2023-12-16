import random

# Zeke Ash
# Intermediate Python - Conference Project
# 12.15.23

# Welcome to HINT: A text-based mystery game for 1-6 Players

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


public_log = []

g = {}

# run the file and enter main() to play game
# character objects are listed at the bottom, feel free to toggle humanPlayer.

def main():
    # setup goes here
    g['gameOver'] = False
    # enter some rules
    # beginning of the turn
    while not g['gameOver']:
        for player in playerList.copy():
            if not g['gameOver']:
                if not player.eliminated:
                    if player.humanPlayer:
                        player.playerTurn()
                    else:
                        player.aiTurn()

class Player:

    def __init__(self, name, location, eliminated=False,humanPlayer=True):
        self.name = name
        self.location = location
        self.location.players.append(self)
        self.notebook = self.createNotebook(deck)
        self.hand = []
        self.eliminated = eliminated
        self.humanPlayer = humanPlayer

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

    def moveTo(self, newLocation):
        self.location.players.remove(self)
        newLocation.players.append(self)
        self.location = newLocation

    def go(self, direction):
        if direction == "none":
            print(f"{self} remains in {self.location}")
        elif direction not in self.location.paths:
            print(f"I don't see how to go {direction} from here.")
        else:
            destination = self.location.paths[direction]
            print(f"{self} moves from {self.location} to {destination}")
            self.moveTo(destination)

    def suggest(self,player,room,weapon):
        return [player,room,weapon]

    def playerTurn(self):
        # tell player possible moves and current location
        print(f"""It is your turn, {self.name}! 
You are in {self.location}!""")
        for direction in self.location.paths:
            otherPlace = self.location.paths[direction]
            print(f"  {direction} to {otherPlace}")
        move = input("which direction would you like to move?")
        self.go(move)
        # check if you are in a room where you can suggest/accuse
        if self.location.canSuggest:
            suggestAction = input(f"""You have {self.hand} in your hand.
Would you like to make a suggestion (type 'yes' if so, 'notebook' if you would like to look at your notebook, 
    "log" to look at public log, or any key to pass)?""")
            if suggestAction != "yes" and suggestAction != "notebook" and suggestAction != "log":
                pass
                #print("passing turn...")
            elif suggestAction == 'notebook':
                self.displayNotebook()
                suggestAction = input("enter 'yes' to make a suggestion, or nothing to pass the turn")
            elif suggestAction == "log":
                for s in public_log:
                    print(s)
                suggestAction = input("enter 'yes' to make a suggestion, or nothing to pass the turn")
            if suggestAction == 'yes':
                suspect = input("which character would you like to suggest (simply type the color)?")
                suspect_object = get_object_by_name(suspect)
                suspect_object.moveTo(self.location)
                print(f"{suspect_object} has been called to the {self.location}")
                # move suspect to location
                weapon = input("""What weapon did they use? 
The weapons are: Candlestick, Dagger, Revolver, Lead pipe, Wrench, Rope""")
                # case insensitive
                self.gatherResponses([suspect_object.name, self.location.name, weapon], playerList.copy())
        else:
            print("You cannot make a suggestion in here!")
        accuseAction = input(f"""{self.name}, would you like to make an accusation?
Remember, if your accusation is wrong, you will be eliminated!
Type 'yes' to make an accusation or 'notebook' to review your notebook. enter nothing to pass the turn.""")
        if accuseAction == "notebook":
            self.displayNotebook()
            accuseAction = input("enter 'yes' to make an accusation, or nothing to pass the turn")
        if accuseAction == "yes":
            finalAccusation = False
            while not finalAccusation:
                suspect = input("which character would you like to accuse (simply type the color)?")
                suspect_object = get_object_by_name(suspect)
                weapon = input("""What weapon did they use? 
    The weapons are: Candlestick, Dagger, Revolver, Lead pipe, Wrench, Rope""")
                room = input("""What room did it happen in?
    The rooms are: Study, Kitchen, Ballroom, Conservatory, Billiard Room,
                              Library, Hall, Lounge, Dining Room""")
                sure = input(f"""Your accusation is: {suspect_object.name}, in the {room}, with the {weapon}.
    Would you like to submit this as your final accusation? 
    enter 'yes' to confirm, any key to edit, or 'cancel' to cancel accusation.""")
                if sure == "yes":
                    self.accuse([suspect_object.name,room,weapon])
                    finalAccusation = True
                elif sure == "cancel":
                    finalAccusation = True
                    print("passing the turn...")
            # has someone responded? == False
            # for player in list (if HSR? == False)
                # chance to respond
                # if response, HSR? == True
        # if no offer to accuse

    def aiTurn(self):
        print(f"It is {self.name}'s turn!")
        direction = random.choice(list(self.location.paths.keys()))
        self.go(direction)
        if self.location.canSuggest:
            suspect = random.choice(deck.playercards)
            weapon = random.choice(deck.weaponcards)
            print(f"{self.name} suggested: {suspect} in the {self.location.name} with the {weapon}.")
            self.gatherResponses([suspect, self.location.name, weapon], playerList.copy())
        if random.randrange(1,30) == 30:
            suspect = random.choice(deck.playercards)
            weapon = random.choice(deck.weaponcards)
            room = random.choice(deck.roomcards)
            self.accuse([suspect,room,weapon])

    def gatherResponses(self, suggestion, players):
        players = list(players)
        selfIndex = players.index(self)
        players = players[selfIndex+1:] + players[:selfIndex]
        for player in players:
            options = []
            for card in player.hand:
                if card in suggestion:
                    options.append(card)
        # if player not human, random.choice(options) (or something smarter)
            if len(options) > 1:
                if not player.humanPlayer:
                    shownCard = random.choice(options)
                    self.updateNotebook(shownCard, player.name, "x")
                    if self.humanPlayer:
                        print(f"{player} shows the card {options[0]}.")
                    else:
                        print(f"{player} shows a card.")
                    public_log.append(f"""{self.name} suggested, {suggestion}.
{player.name} showed something""")
                    return shownCard
                cue = input(f"{player}, you have some of the suggested cards. Press any key to choose one to show.")
                print(options)
                shownCard = input(f"""{self.name} suggested {suggestion}. You have {options}.
Which card would you like to show {self.name}?""")
                self.updateNotebook(shownCard, player.name, "x")
                if self.humanPlayer:
                    print(f"{player} shows the card {options[0]}.")
                else:
                    print(f"{player} shows a card.")
                public_log.append(f"""{self.name} suggested, {suggestion}.
{player.name} showed something""")
                return shownCard
            elif len(options) == 1:
                if self.humanPlayer:
                    print(f"{player} shows the card {options[0]}.")
                else:
                    print(f"{player} showed a card.")
                self.updateNotebook(options[0],player.name,"x")
                public_log.append(f"""{self.name} suggested, {suggestion}.
{player.name} showed something""")
                return options[0]
            else:
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
            print(f"You guessed {envelope} correctly! You win!")
            g['gameOver'] = True
        else:
            print(f"{self.name} guessed wrong and is out of the game!")
            self.eliminated = True
            playersLeft = []
            for player in playerList.copy():
                if not player.eliminated:
                    playersLeft.append(player)
            if len(playersLeft) == 1:
                print(f"{playersLeft[0]} is the last player standing! Congratulations {playersLeft[0]}!")
                g['gameOver'] = True

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



class Place:

    # constructor
    def __init__(self, name, canSuggest = True):
        self.name = name
        self.paths = {}
        self.players = []
        self.canSuggest = canSuggest

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


# set up board, cards, and characters

deck = Deck()

envelope = deck.prepPerp(random.choice(deck.playercards),random.choice(deck.roomcards),random.choice(deck.weaponcards))
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

corridor1 = Place("Corridor", canSuggest=False)
corridor2 = Place("Corridor", canSuggest=False)
corridor3 = Place("Corridor", canSuggest=False)
corridor4 = Place("Corridor", canSuggest=False)

scarlet = Player("Miss Scarlet", corridor1)
peacock = Player("Mrs. Peacock", corridor2, humanPlayer=False)
mustard = Player("Colonel Mustard", corridor3, humanPlayer=False)
green = Player("Mr. Green", corridor3, humanPlayer=False)
white = Player("Mrs. White", corridor4, humanPlayer=False)
plum = Player("Prof. Plum", corridor1, humanPlayer=False)

playerList = {scarlet,peacock,plum,mustard,green,white}

corridor1.connect("south", corridor2)
corridor2.connect("south", corridor3)
corridor3.connect("south", corridor4)

corridor1.connect("east", lounge)
corridor1.connect("west", study)
corridor1.connect("north", hall)

corridor2.connect("east", library)
corridor2.connect("west", diningRoom)

corridor3.connect("east", ballroom)
corridor3.connect("west", billiardRoom)

corridor4.connect("east", kitchen)
corridor4.connect("west", conservatory)
# dealing cards:

for player in playerList:
    for r in range(3):
        card = random.choice(deck.deck)
        player.hand.append(card)
        deck.deck.remove(card)
    #print(f"{player}'s hand: {player.hand}")
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


