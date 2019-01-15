#
# BlackJack : NAF Culmination Project
# Authors: John Huang, Lisa Oommen, Logan Short, and Connor McQuillen
# January 3, 2018
# 
# Bugs: 
#
from random import randint
import time

class Card:
    def __init__(self, num, suit):
        #Set Number and name it if it's a royal and set value of cards
        if num == 1:
            self.num = 'Ace'
            self.value = num
        elif num <= 10:
            self.num = num
            self.value = num
        elif num == 11:
            self.num = 'Jack'
        elif num == 12:
            self.num = 'Queen'
        elif num == 13:
            self.num = 'King'
        #Set value of cards
        if num >= 11:
            self.value = 10
        #Set suit
        if suit == 1:
            self.suit = 'Hearts'
        elif suit == 2:
            self.suit = 'Diamonds'
        elif suit == 3:
            self.suit = 'Spades'
        elif suit == 4:
            self.suit = 'Clubs'
#String constructor for card name
def cardName(card):
    return f'{card.num} of {card.suit}'

#Create Deck
deck = []
#Add cards to deck
for i in range(1,5):
    for n in range(1,14):
        card = Card(n, i)
        deck.append(card)

#Set arrays for hands
dealersHand = []
playersHand = []
p = playersHand
d = dealersHand

#Shuffle deck method
def shuffleDeck(deck):
    for i in deck:
        deck.remove(i)
        deck.insert(randint(0, 52), i)

#Draw a card method
def drawCard(hand, deck):
    c = deck[len(deck) - 1]
    deck.remove(c)
    hand.append(c)

#Get value of a hand
def handValue(hand):
    aces = 0
    nonAceSum = 0
    realSum = 0
    for c in hand:
        if c.num == 'Ace':
            aces += 1
        else:
            nonAceSum += c.value
    
    realSum = nonAceSum + aces
    if (nonAceSum > 21) or (realSum >= 21):
        #If value of hand without aces is over 21 then give the lowest possible hand value
        #Or
        #If value of hand with aces all at a value of 1 is over or equal to 21 then give the lowest possible hand value
        return realSum
    else:
        #No more than 1 ace can have a value of over 11 in a hand or else it busts so if it doesn't bust then return that value
        #If it does bust then return the lowest possible value.
        realSum = nonAceSum + 11 + aces - 1
        if realSum < 22:
            return realSum
        else:
            realSum = nonAceSum + aces
            return realSum

#Show cards in a hand
def showCards(hand):
    showCards = ' a '
    handPos = 0
    for cd in hand:
        handPos += 1
        if handPos == len(p):
            showCards = showCards + f'and {cardName(cd)}'
        else:
            showCards = showCards + f'{cardName(cd)}, '
    return showCards

#Check for bust
def bust(hand):
    if handValue(hand) > 21:
        return True
    else:
        return False

#Game Starts
print()
print("BlackJack game is starting...\n")

play = True
while play:
    print("Dealer shuffles cards...\n")
    shuffleDeck(deck)

    print("Dealer deals cards...\n")
    for i in range (0,2):
        #Give each player 2 cards
        drawCard(p, deck)
        drawCard(d, deck)
    time.sleep(0.5)

    print(f'The dealer is showing a {cardName(d[1])}.\n')

    #Player turn
    print("Player turn starts...\n")
    playerBust = False
    while not playerBust:
        #Show players cards
        print('You have' + showCards(p) + '\n')
        userInput = input("Would you like another card? (Y/N)")
        if userInput.lower() == 'y':
            #Add another card to players hand
            drawCard(p, deck)
            print(f'You are given a {cardName(p[len(p) - 1])}.')

            #Check if busted
            playerBust = bust(p)
            if playerBust:
                print(f'You busted! The lowest value of your hand was {handValue(p)}.')
        elif userInput.lower() == 'n':
            break
        else:
            print(f'Invalid input: {userInput}. No action taken.\n')
    
    #Computer turn
    if not playerBust:
        print("\nDealer turn starts...")
        #Limit for which the computer keeps going for more cards
        limit = randint(16, 19)
        dealerBust = False
        while not dealerBust:
            print("The dealer is thinking.")
            time.sleep(1.5)
            if handValue(d) < limit:
                drawCard(d, deck)
                print(f'The dealer drew a {cardName(d[len(d) - 1])}.\n')
                #Check if busted
                dealerBust = bust(d)
                if dealerBust:
                    print(f"The dealer busted! The lowest value of the dealer's hand was {handValue(d)}.")
            else:
                break

        time.sleep(0.5)
        #Determine winner
        win = "Congratulations player 1!\nYou have won!\n"
        lost = "Sorry player 1, you have lost.\n"
        tie = "You and the dealer have tied"
        if dealerBust:
            print(win)
        else:
            if handValue(p) > handValue(d):
                print(win)
            elif handValue(p) < handValue(d):
                print(lost)
            elif handValue(d) == 21 and len(d) == 2:
                print("The dealer had BlackJack!\n")
                print(lost)
            elif handValue(p) == 21 and len(p) == 2:
                print("You had BlackJack!\n")
                print(win)
            elif handValue(p) == handValue(d):
                print(tie)
            else:
                print("ELSE STATEMENT REACHED--------------------------")
    else:
        time.sleep(0.5)
        print("Sorry player 1, you have lost.\n")
    print(f'Dealers hand: {handValue(d)}')
    print(f'Dealers hand: {showCards(d)}\n')

    print(f'Players hand: {handValue(p)}')
    print(f'Players hand: {showCards(p)}\n')

    while True:
        userIn = input(f'\nWould you like to play again? (Y/N)')
        if userIn.lower() == 'y':
            print("Dealer is reseting cards...")
            #Remove cards from player and dealer's hands and put back into deck
            length = len(p)
            for i in range(1, length + 1):
                cd = p[length - i]
                p.remove(cd)
                deck.append(cd)

            length = len(d)
            for i in range(1, length + 1):
                cd = d[length - i]
                d.remove(cd)
                deck.append(cd)
            
            time.sleep(0.5)
            #If not reset correctly then recreate deck and hands
            if (not len(playersHand) == 0) or (not len(dealersHand) == 0) or (not len(deck) == 52):
                print('DealersHand: ' + f'{len(dealersHand)}')
                print('playersHand: ' + f'{len(playersHand)}')
                print('Deck: ' + f'{len(deck)}')
                print("RESETTING EVERYTHING FOR SOME REASON_______________________________________")
                time.sleep(3)
                playersHand.clear()
                dealersHand.clear()
                deck = []
                for i in range(1,5):
                    for n in range(1,14):
                        card = Card(n, i)
                        deck.append(card)
            #Shuffle deck
            shuffleDeck(deck)
            break
        elif userIn.lower() == 'n':
            play = False
            print("Blackjack game has ended... ")
            break
        else:
            print(f'Invalid input: {userIn}. Please try again.')
