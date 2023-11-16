import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two':2, 'Three':3, 'Four':4, 'Five':5, 'Six':6, 'Seven':7, 'Eight':8, 'Nine':9, 'Ten':10, 'Jack':10,
         'Queen':10, 'King':10, 'Ace':11}
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
        self.all_cards = [] 
        for suit in suits:
            for rank in ranks:
                self.all_cards.append(Card(suit,rank))
                
    def shuffle(self):
        random.shuffle(self.all_cards)
        
    def deal(self):
        return self.all_cards.pop()    

class Hand:
    def __init__(self):
        self.cards = []  # start with an empty list as we did in the Deck class
        self.value = 0   # start with zero value
        self.aces = 0    # add an attribute to keep track of aces

    def add_card(self, card):
        self.cards.append(card)
        self.value += values[card.rank]
        if card.rank == "Ace":
            self.aces += 1

    def adjust_for_ace(self):
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


    
class Chips:
    def __init__(self):
        self.total = 100
        self.bet = 0

    def win_bet(self):
        self.total += self.bet

    def lose_bet(self):
        self.total -= self.bet

    def take_bet(self):
        while True:
            try:
                self.bet = int(input("How many chips would you like to bet? "))
                if self.bet <= 0:
                    print("Please enter a bet greater than 0.")
                    continue
                elif self.bet > self.total:
                    print(f"Sorry, your bet can't exceed {self.total}.")
                else:
                    break
            except ValueError:
                print("Please enter a valid integer.")
                continue


def hit(deck, hand):
    single_card = deck.deal()
    hand.add_card(single_card)
    hand.adjust_for_ace()
    
def hit_or_stand(deck, player_hand):
    global playing  # to control an upcoming while loop

    while playing:
        choice = input("Do you want to Hit or Stand? Enter 'h' or 's': ").lower()

        if choice == 'h':
            hit(deck, player_hand)
            show_some(player_hand, dealer_hand)  # Show player's hand after hitting
            if player_hand.value > 21:
                print("Player busts! Dealer wins.")
                player_chips.lose_bet()
                playing = False  # Player busted, exit the loop
        elif choice == 's':
            print("Player stands. Dealer's turn.")
            playing = False
            break  # Move the break statement here
        else:
            print("Invalid input. Please enter 'h' or 's'.")
            continue



def show_some(player, dealer):
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print(f"Total value: {player.value}\n")

    print("Dealer's Hand:")
    print("Hidden Card")
    for card in dealer.cards[1:]:
        print(card)
    print("\n")

def show_all(player, dealer):
    print("\nPlayer's Hand:")
    for card in player.cards:
        print(card)
    print(f"Total value: {player.value}\n")

    print("Dealer's Hand:")
    for card in dealer.cards:
        print(card)
    print(f"Total value: {dealer.value}\n")
    
def player_busts(player, dealer, chips):
    print("Player busts! Dealer wins.")
    chips.lose_bet()

def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()

def dealer_busts(player, dealer, chips):
    print("Dealer busts! Player wins.")
    chips.win_bet()

def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()

def push():
    print("It's a tie! The game is a push.")
    
# Initialize player's chips outside the game loop
player_chips = Chips()

while True:
    print("Welcome to Blackjack!\n")

    # Create & shuffle the deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # Prompt the Player for their bet
    player_chips.take_bet()

    # Reset playing for a new game
    playing = True

    while playing:
        # Show cards (but keep one dealer card hidden)
        show_some(player_hand, dealer_hand)

        # Prompt for Player to Hit or Stand
        hit_or_stand(deck, player_hand)

        # If player's hand exceeds 21, run player_busts() and break out of the loop
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)
            break

        # If Player hasn't busted, play Dealer's hand until Dealer reaches 17
        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # Show all cards
        show_all(player_hand, dealer_hand)

        # Run different winning scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif player_hand.value > dealer_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        elif player_hand.value < dealer_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        else:
            push()

        # Inform Player of their chips total
        print(f"\nPlayer's total chips: {player_chips.total}")

        # Ask to play again
        play_again = input("Do you want to play again? Enter 'y' or 'n': ").lower()
        if play_again != 'y':
            print("Thanks for playing! Goodbye.")
            playing = False  # Add this line to ensure the outer loop terminates
            break


        # Reset hands for a new round
        player_hand = Hand()
        dealer_hand = Hand()
        playing = False  # Set playing to False to exit the inner loop and prompt for a new bet







