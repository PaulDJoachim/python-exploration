import random


suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Ace', 'Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King')
values = {'Ace': 11, 'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9,
          'Ten': 10, 'Jack': 10, 'Queen': 10, 'King': 10}


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(str(Card(suit, rank)))

    def __str__(self):
        return str(self.deck)

    def shuffle(self):
        random.shuffle(self.deck)

    def deal(self):
        # return and remove the last card from the deck list
        return self.deck.pop()


class Hand:

    def __init__(self):
        self.cards = []
        self.value = 0
        self.aces = 0
        # dealer_value is the value of only the first card in the hand (for showing the player)
        self.dealer_value = 0

    def __str__(self):
        return str(self.cards)

    def add_card(self, card):
        # add a popped card from the game_deck list to the self.cards list
        self.cards.append(card)

        # check if the last card added is an ace, add 1 to the ace counter if so.
        if self.cards[-1].split()[0] == 'Ace':
            self.aces += 1

        # Adds the value of the card to the Hand's self.value
        self.value += values[card.split(' ', 1)[0]]
        # This value is shown to the player since they only see one of the dealer's 2 initial cards
        self.dealer_value = values[self.cards[0].split(' ', 1)[0]]
        # If value goes over 21 subtract 10 if at least one ace has been dealt. Remove an ace counter from self.aces
        while self.value > 21 and self.aces != 0:
            self.value -= 10
            self.aces -= 1


class Player:

    def __init__(self, money=100):
        self.money = money

    def gain(self, amount):
        self.money += amount

    def lose(self, amount):
        self.money -= amount


def get_bet(money):
    print(f'You have ${money}')
    # Double Loops which make sure the wager input is a number and the player has enough money to cover the bet.
    while True:
        while True:
            try:
                wager = int(input('What amount will you wager: \n$'))
                break
            except:
                print('Oops, that doesn\'t look like a number!')
        if wager > money:
            print('Sorry, you don\'t have that much to wager')
        else:
            return wager


def show_cards(player_hand, dealer_hand):
    print(f'You have been dealt the {player_hand.cards[0]} and the {player_hand.cards[1]} '
          f'for a total value of {player_hand.value}.')
    print(f'The dealer is showing the {dealer_hand.cards[0]} for a total of {dealer_hand.dealer_value}.')


# if player hits will add a card, print the total, ask to hit or stay again.
def hit_or_stay(player_hand, game_deck):
    while True:
        choice = input('Hit or Stay?\n').lower()
        if choice == 'hit':
            player_hand.add_card(game_deck.deal())
            print(f'The dealer deals the {player_hand.cards[-1]}\n'
                  f'your new total is :{player_hand.value}')
            return True
        elif choice == 'stay':
            return False
        else:
            print('Please type Hit or Stay')


def bust_check(player_hand, game_player, wager):
    if player_hand.value > 21:
        print('You busted!')
        game_player.lose(wager)
        print(f'You lost ${wager} and have ${game_player.money} left.')
        print('Would you like to bet again? (Y/N)')
        choice = input()
        if choice.lower() == 'y':
            return True
        else:
            return False


def player_turn(player_hand, game_deck, game_player, wager):
    while hit_or_stay(player_hand, game_deck):
        if bust_check(player_hand, game_player, wager):
            break


def dealer_turn(dealer_hand, game_deck, wager, game_player):
    print(f'The dealer reveals their second card was {dealer_hand.cards[1]} for a total '
          f'value of {dealer_hand.value}.')
    while dealer_hand.value < 17:
        dealer_hand.add_card(game_deck.deal())
        print(f'The dealer draws the {dealer_hand.cards[-1]}\n'
              f'their new total is :{dealer_hand.value}')
    if dealer_hand.value > 21:
        print('The dealer busted, you win!')
        game_player.gain(wager)
        print(f'You now have ${game_player.money}')


def check_winner(dealer_hand, player_hand, game_player, wager):
    if dealer_hand.value > player_hand.value:
        game_player.lose(wager)
        print(f'The dealer\'s {dealer_hand.value} beats your {player_hand.value}\n'
              f'You lose ${wager}.\n'
              f'You now have ${game_player.money}')
    elif player_hand.value > dealer_hand.value:
        game_player.gain(wager)
        print(f'Your {player_hand.value} beats the dealer\'s {dealer_hand.value}\n'
              f'You win ${wager}!'
              f'You now have ${game_player.money}')


def main():
    # 1.Create a deck of 52 cards
    game_player = Player()
    game_deck = Deck()
    playing = True

    while playing:

        # 2.Shuffle the deck
        game_deck.shuffle()

        # 3.Ask the Player for their bet
        # 4.Make sure that the bet does not exceed bankroll
        wager = get_bet(game_player.money)

        # 5.Deal two cards to the Dealer and two to the player
        player_hand = Hand()
        dealer_hand = Hand()
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())
        player_hand.add_card(game_deck.deal())
        dealer_hand.add_card(game_deck.deal())

        # 6.Show only one of the Dealer cards
        # 7.Show both player cards
        show_cards(player_hand, dealer_hand)

        # 8. Ask the Player if they wish to Hit, and take another card
        # 9.If the Player's hand doesn't Bust ask if they want to hit again.
        player_turn(player_hand, game_deck, game_player, wager)

        # If the player did not bust during "player_turn" the dealer will take cards
        # until they have 17 or more.
        if player_hand.value <= 21:
            dealer_turn(dealer_hand, game_deck, wager, game_player)

            # If the dealer did not bust during "dealer_turn" we compare the value of dealer
            # against the player and change the player's money depending on the wager.
            if dealer_hand.value <= 21:
                check_winner(dealer_hand, player_hand, game_player, wager)

        # 12. Ask to play another hand


main()
