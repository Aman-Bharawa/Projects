import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10, 'Queen':10, 'King':10, 'Ace':11}

playing = True

class Card:
    
    def __init__(self,suit,rank):
        self.suit = suit
        self.rank = rank
        self.value = values[rank]
    
    def __str__(self):
        return self.rank + ' of ' + self.suit
    
class Deck:
    
    def __init__(self):
        self.deck = []  # start with an empty list
        for suit in suits:
            for rank in ranks:
                created_card = Card(suit,rank)
                self.deck.append(created_card)
    
    def __str__(self):
        return '\n'.join(str(cards) for cards in self.deck)  
    
    '''
    deck_comp =' '
    for card in self.deck:
       deck_comp += '\n' + card.__str__()
    return "the deck has: "+deck_comp
    '''
            

    def shuffle(self):
        random.shuffle(self.deck)
        
    def deal(self):
        single_card = self.deck.pop()
        return single_card
    
class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of number of aces
    
    def add_card(self,card):
        #card passed in
        #from Deck.deal()---> single card(suit ,rank)
        self.cards.append(card)
        self.value += values[card.rank]

        #track aces
        if card.rank == 'Ace':
            self.aces += 1
    
    def adjust_for_ace(self):
        #if total value >21 and i still have an ace
        #than change my ace to be a 1 instead of an 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1

class Chips:
    
    def __init__(self,total=100):
        self.total = total # This can be set to a default value or supplied by a user input
        self.bet = 0
        
    def win_bet(self,chip):
        self.total += self.bet
    
    def lose_bet(self):
        self.total -= self.bet

def take_bet(chips):
    while True:
        try:
            chips.bet = int(input("how many chips would you like to bet? "))
        except:
            print("sorry please provide an integer")
        else:
            if chips.bet > chips.total:
                print("sorry , you do not have enough chips! you have :{}".format(chips.total))
            else:
                break

        
def hit(deck,hand):
    hand.add_card(deck.deal())
    hand.adjust_for_ace()

def hit_or_stand(deck,hand):
    global playing  # to control an upcoming while loop
    
    while True:

        x = input('hit or stand ?enter h and s ')

        if x[0].lower() == 'h':
            hit(deck,hand)
        elif x[0].lower() =='s':
            print("player stands dealer's turn")
            playing = False
        else:
            print('sorry,i did not understand that,please enter h or s only!')
            continue
        break

def show_some(player,dealer):

    #dealer.card[0]

    #show only one of the dealer's cards
    print("\n Dealer's Hand: ")
    print("first card hidden! ")
    print(dealer.cards[1])

    #show all (2 cards) of the player's hand/cards
    print("\n player's hand:")
    for card in player.cards:
        print(card)

def show_all(player,dealer):

    #show all (2 cards) of the dealer's hand/cards
    print("\n dealer's hand:")
    for card in dealer.cards:
        print(card)

    ##print("/n dealer's hand: ",*dealer.cards,sep ='\n')   any do like this

    #calculate and display value
    print(f"value of dealer's hand is : {dealer.value}")
    #show all (2 cards) of the player's hand/cards
    print("\n player's hand:")
    for card in player.cards:
        print(card)
    print(f"value of player's hand is : {player.value}")

def player_busts(player,dealer,chips):
    print("bust player!")
    chips.lose_bet()

def player_wins(player,dealer,chips):
    print('player wins!')
    chips.win_bet()

def dealer_busts(player,dealer,chips):
    print('player wins,dealer busted!')
    chips.win_bet()
    
def dealer_wins(player,dealer,chips):
    print("dealer wins!")
    chips.lose_bet()
    
def push(player,dealer,chips):
    print('dealer and player tie! PUSH')

while True:
    # Print an opening statement
    print("welcome to blackjack")
    
    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())
    
        
    # Set up the Player's chips
    player_chips = Chips()
    
    
    # Prompt the Player for their bet
    take_bet(player_chips)
    
    # Show cards (but keep one dealer card hidden)
    show_some(player_hand,dealer_hand)
    
    while playing:  # recall this variable from our hit_or_stand function
        
        # Prompt for Player to Hit or Stand
        hit_or_stand(deck,player_hand)
        
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand,dealer_hand)
        
        # If player's hand exceeds 21, run player_busts() and break out of loop
        if player_hand.value > 21:
            player_busts(player_hand,dealer_hand,player_chips)


            break

    # If Player hasn't busted, play Dealer's hand until Dealer reaches 17 (soft 17 rule of official game),can write 17 in place player_hand
    if player_hand.value <= 21:

        while dealer_hand.value < player_hand.value:
            hit(deck,dealer_hand)
        
    
        # Show all cards
        show_all(player_hand,dealer_hand)
    
        # Run different winning scenarios
        if dealer_hand.value >21:
            dealer_busts(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value>player_hand.value:
            dealer_wins(player_hand,dealer_hand,player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand,dealer_hand,player_chips)
        else:
            push(player_hand,dealer_hand)
    
    # Inform Player of their chips total 
    print("\n player total chips are at:{}".format(player_chips.total))
    # Ask to play again
    new_game = input("would you like to play another hand? y/n")
    
    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print('thank you for playing')
        break
    