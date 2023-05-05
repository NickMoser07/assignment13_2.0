from time import sleep
from modules.deck import Deck
from modules.card import Card
def main():

    valid = False
    while not valid:
        playerCount = input("how many players will be playing blackjack (1, 5):  ")
        
        try:
            int(playerCount)
        except:
            print("That is not a valid input")
        else:
            valid = True
            playerCount = int(playerCount)
        if playerCount < 1 or playerCount > 5:
                    print("That number of players is not accepted")
                    valid = False

    #init balances and bet lists
    balances = [100 for i in range(playerCount)]
    bets = [0 for i in range(playerCount)]
    
    
    #balances[2] = 0
    
    done = False
    while not done:
        hands = [[] for i in range(len(balances)+1)]
        values = [0 for i in range(len(balances)+1)]
        for i in range(len(balances)):      #checks if any players do not have funds required
            if balances[i] <= 0:
                balances[i] = False
                print("player " + str(i+1) + " is out of money and can no longer play")
        everybodyOut = True
        for i in balances:
            if i != False:
                everybodyOut = False
        if everybodyOut:
            print("Nobody had any money left")
            done = True
        for player in range(len(balances)):
            if balances[player]:
                print("Player " + str(player+1) + " has $" + str(balances[player]))
                
        for i in range(len(balances)):      #prompt users for their bet amount
            if balances[i]:
                print("\n\nit is player "+str(i+1)+"'s turn to bet\nyou have $"+str(balances[i]))
                valid = False
                while not valid:
                    bet = input("how much would you like to bet:  ")
                    sleep(1)
                    
                    try:
                        float(bet)
                    except:
                        print("That is not a valid bet\n")
                        sleep(1)
                    else:
                        valid = True
                        bet = float(bet)
                        if balances[i] < 5:
                            bet = balances[i]
                            print("Your balance is below $5. your bet has been set to $" + str(balances[i]))
                            sleep(1)
                        if bet < 5 and balances[i] > 5:
                            bet = 5
                            print("That bet is too low. your bet has been increased to $5")
                            sleep(1)
                        if bet > balances[i]:
                            bet = balances[i]
                            print("you do not have the funds for that. your bet has been set to $" + str(balances[i]))
                            sleep(1)
                        bets[i] = bet
            elif balances[i]:
                continue
        deck = Deck()
        for i in range(2):      #drawing cards
            print("\n")
            for i in range(len(balances)):
                if balances[i] != False:
                    drew = deck.draw()
                    print("\nplayer " + str(i+1) + " drew " + str(drew))
                    sleep(0.25)
                    drewValue = drew.getCardValue()
                    if drew.getCardValue() > 10:
                        drewValue = 10
                    if drew.getCardValue() == 1:
                        drewValue = 11
                    #print(str(drewValue))
                    print("")
                    values[i+1] += drewValue
                    hands[i+1].append(drew)

                        
            drew = deck.draw()
            hands[0].append(drew)
            print("The dealer has drawn a card\n")
        print("The dealer has " + str(hands[0][1]))       #dealer reveals first card
        for player in range(len(balances)):
            if balances[player] != False:
                held = False
                for i in hands[player+1]:
                    if i.getRank() == "Ace" and values[player+1] > 21:
                        values[player+1] -= 10      #set the value of the ace to one if the value of the hand is above 21
                
                
                while not held:
                    print("\n\t\tPlayer " + str(player+1) + "'s Turn:\n\nYour hand is:")
                    for i in hands[player+1]:
                        print(str(i))
                    if values[player+1] > 21:
                        print("You lose. you went past 21\nYour total was "+ str(values[player+1]), end="\n\n")
                        sleep(1)
                        past21 = True
                        break
                    else:
                        past21 = False
                    if not past21:
                        print("you are at " + str(values[player+1]))
                        print("1) Hit\n2) Hold")
                        sleep(1)
                        valid = False
                        while not valid:    #input catching
                            choice = input("1 or 2 ( ")
                            if choice != "1" and choice != "2":
                                print("That is not a valid input")
                            else:
                                choice = int(choice)
                                valid = True
                        
                        if choice == 1:
                            print("you chose hit\n")
                            drew = deck.draw()
                            hands[player+1].append(drew)
                            print("you drew " + str(drew))
                            if drew.getCardValue() == 1:
                                if values[player+1] + 11 > 21:
                                    values[player+1] += 1
                                else:
                                    values[player+1] += 11
                            elif drew.getCardValue() > 10:
                                values[player+1] += 10
                            
                            else:
                                values[player+1] += drew.getCardValue()
                            
                        elif choice == 2:
                            print("You chose Hold\n\n")
                            held = True

        for card in hands[0]:
            if card.getCardValue() > 10:    
                values[0] += 10
            elif card.getCardValue() == 1 and values[0] + 11 > 21:
                values[0] += 1
            else:
                values[0] += card.getCardValue()
        dealerover17 = values[0] > 17
        while not dealerover17:
            
            drew = deck.draw()
            hands[0].append(drew)
            if drew.getCardValue() > 10:
                values[0] += 10
            if drew.getCardValue() == 1:
                if values[0] + 11 > 21:
                    values[0] += 1
                else: 
                    values[0] += 11
            else:
                values[0] += drew.getCardValue()
            dealerover17 = values[0] > 17
        print("The dealer got "+ str(values[0]) + " in total")
        for player in range(len(balances)):
            if balances[player]:
                notBust = values[player+1] <= 21
                dealerBust = values[0]>21
                if notBust and dealerBust:
                    print("player " + str(player+1) + " won $" + str(bets[player]) + " with " + str(values[player+1]))
                    balances[player] += bets[player]
                elif notBust and values[0] < values[player+1]:
                    print("player " + str(player+1) + " won $" + str(bets[player]) + " with " + str(values[player+1]))
                    balances[player] += bets[player]
                elif values[0] == values[player+1] and notBust:
                    print("player "+ str(player+1) + " tied with the dealer and won nothing with " + str(values[player+1]))
                else:
                    print("player " + str(player+1) + " lost to the dealer and lost $" + str(bets[player]) + " with " + str(values[player+1]))
                    balances[player] -= bets[player]
        valid = False
        while not valid:   
            if everybodyOut:
                done = True
                print("Everybody is out of money")
                Valid = True
                break 
            choice = input("\n\n\t\tWould you like to play again? y/n:  ")
            if choice != "y" and choice != "n":
                print("That is not a valid choice")
            else:
                valid = True
        done = choice == "n"    
        if done:
            print("\n\n\tThe winners are:\n")
            everybodyOut = True
            for i in balances:
                if i != False:
                    everybodyOut = False
            if everybodyOut:
                print("The Dealer.....")
                done = True
            else:
                scores = {}
                for i in range(len(balances)):
                    if balances[i]:
                        scores[balances[i]] = "Player " + str(i+1)
                dictBalances = list(scores.keys())
                dictBalances.sort(reverse=True)
                for account in dictBalances:
                    print(str(scores[account]) + ": $" + str(account))

                print("\nThanks for playing!")
            
                
        
main()