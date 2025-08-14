# Project Title: LET'S PLAY ROCK PAPER SCISSORS FROM AROUND THE WORLD ! ! ! !

# imported libraries
from pyfiglet import Figlet
fig = Figlet()
from printy import printy
import random
import sys

# Displays a header for user
def graphic():
    printy(fig.renderText("|   Let's Play  Rock   |"), "wB")
    printy(fig.renderText("|   Paper  Scissors   |"), "wB")
    printy(fig.renderText("|   From    Around   |"), "wB")
    printy(fig.renderText("|   The    World ! ! ! !   |"), "wB")

# Prompts user if they're ready
def ready():
    print("+-----------------------------------------------------------------------------+")
    while True:
        ready = input("|                     Are you ready? (Yes/No): ").strip().title()
        if ready == "Yes":
            break
        # perform safe exit out if not
        elif ready == "No":
            printy(fig.renderText("|           Come Back           |"), "oB")
            printy(fig.renderText("| When Ready ! ! ! |"), "oB")
            sys.exit()
        else:
            continue

# displays chart for user
def chart():
    print("+-----------------------------------------------------------------------------+")
    print("|                     What country are you interested in?                     |")
    print("|    Write the clause preceding the paranthesis to play that variation :D     |")
    print("+-----------------------------------------------------------------------------+")
    print("|                                   Western                                   |")
    print("|                        Vanilla) Rock Paper Scissors                         |")
    print("|                      American Historical) Ro-Sham-Beau                      |")
    print("|                           Hawaii) Guu Paa Choki                             |")
    print("+-----------------------------------------------------------------------------+")
    print("|                                   Eastern                                   |")
    print("|                         Japan) Namekuji Kawazu Hebi                         |")
    print("|                              China) Shi Bu Ka                               |")
    print("|                              Korea) Kai Bai Bo                              |")
    print("+-----------------------------------------------------------------------------+")
    print("|                                  European                                   |")
    print("|                         Finland) Kivi Sakset Paperi                         |")
    print("|                        France) Pierre Papier Ciseaux                        |")
    print("|                         Spain) Piedra Papel Tijera                          |")
    print("+-----------------------------------------------------------------------------+")

# gets user's country of interest
def getCountry():
    while True:
        country = input("|                              Country: ").strip().title()
        if country in ["Vanilla", "American Historical", "Hawaii", "Japan", "China", "Korea", "Finland", "France", "Spain"]:
            break
        else:
            continue
    print("+-----------------------------------------------------------------------------+")
    return country

# displays game rules if prompted yes
def getRules():
    while True:
        rules = input("|             Would you like to see the rules? (Yes/No) ").strip().title()
        if rules == "Yes":
            print ("|    It's a two-player game where both humans throw a certain hand sign in    |")
            print ("|    unison and they \"face off\" against each other. Each of the signs have    |")
            print ("|   one strength and one weakness. If the same sign is thrown, the round is   |")
            print ("|  nullified and ignored. It's generally played \"best to three\" and whomever  |")
            print ("|   wins thrice is dictatated as the winner. It's generally a child's game.   |")
            break
        elif rules == "No":
            break
        else:
            continue
    print("+-----------------------------------------------------------------------------+")

# displays specific rules based on user's variation
def getSpecificRules(country):
    # "if" cases for all variations
    if country == "Vanilla":
        # generates list of "players" in specified variation
        itemList = ["Rock", "Paper", "Scissors"]
        # displays specific rules
        print("|   \"" + itemList[0] + "\" beats \"" + itemList[2] +
                "\", \"" + itemList[1] + "\" beats \"" + itemList[0] +
                "\", \"" + itemList[2] + "\" beats \"" + itemList[1] + "\"   |")
    elif country == "American Historical":
        itemList = ["Ro", "Beau", "Sham"]
        print("|          \"" + itemList[0] + "\" beats \"" + itemList[2]
                + "\", \"" + itemList[1] + "\" beats \"" + itemList[0] + "\", \""
                + itemList[2] + "\" beats \"" + itemList[1] + "\"          |")
    elif country == "Hawaii":
        itemList = ["Guu", "Paa", "Choki"]
        print("|         \"" + itemList[0] + "\" beats \"" + itemList[2]
                + "\", \"" + itemList[1] + "\" beats \"" + itemList[0] + "\", \""
                + itemList[2] + "\" beats \"" + itemList[1] + "\"         |")
    elif country == "Japan":
        itemList = ["Kawazu", "Hebi", "Namekuji"]
        print("|  \"" + itemList[0] + "\" beats \"" + itemList[2] +
                "\", \"" + itemList[1] + "\" beats \"" + itemList[0] +
                "\", \"" + itemList[2] + "\" beats \"" + itemList[1] + "\"  |")
    elif country == "China":
        itemList = ["Shi", "Ka", "Bu"]
        print("|             \"" + itemList[0] + "\" beats \"" + itemList[2]
                + "\", \"" + itemList[1] + "\" beats \"" + itemList[0] + "\", \""
                + itemList[2] + "\" beats \"" + itemList[1] + "\"             |")
    elif country == "Korea":
        itemList = ["Bai", "Bo", "Kai"]
        print("|            \"" + itemList[0] + "\" beats \"" + itemList[2]
                + "\", \"" + itemList[1] + "\" beats \"" + itemList[0] + "\", \""
                + itemList[2] + "\" beats \"" + itemList[1] + "\"            |")
    elif country == "Finland":
        itemList = ["Kivi", "Paperi", "Sakset"]
        print("|    \"" + itemList[0] + "\" beats \"" + itemList[2] +
                "\", \"" + itemList[1] + "\" beats \"" + itemList[0] +
                "\", \"" + itemList[2] + "\" beats \"" + itemList[1] + "\"    |")
    elif country == "France":
        itemList = ["Pierra", "Papier", "Ciseaux"]
        print("| \"" + itemList[0] + "\" beats \"" + itemList[2] +
                "\", \"" + itemList[1] + "\" beats \"" + itemList[0] +
                "\", \"" + itemList[2] + "\" beats \"" + itemList[1] + "\" |")
    elif country == "Spain":
        itemList = ["Piedra", "Papel", "Tijera"]
        print("|   \"" + itemList[0] + "\" beats \"" + itemList[2] +
                "\", \"" + itemList[1] + "\" beats \"" + itemList[0] +
                "\", \"" + itemList[2] + "\" beats \"" + itemList[1] + "\"   |")
    print("+-----------------------------------------------------------------------------+")
    return itemList

def ready2():
    # infinite loop for input validation
    while True:
        # check if user is ready
        ready2 = input("|                 Are you ready FOR SURE? (Yes/No): ").strip().title()
        if ready2 == "Yes":
            printy(fig.renderText("|   Game  Time  ! ! !   |"), "oB")
            break
        # perform safe exit out if not
        elif ready2 == "No":
            printy(fig.renderText("|           Come Back           |"), "oB")
            printy(fig.renderText("| When Ready ! ! ! |"), "oB")
            sys.exit()
        else:
            continue

# meat of the program
def playGame(itemList):
    print("+-----------------------------------------------------------------------------+")
    # iterable variables for robo and human
    userWinCount = 0
    roboWinCount = 0
    roundsPlayed = 0
    # infinite loop for input validation
    while True:
        # returns userWins and roboWins the moment either hits 3
        if userWinCount >= 3 or roboWinCount >= 3:
            return userWinCount, roboWinCount, roundsPlayed
        # ask for input
        ans = input("|                               Throw your sign: ").strip().title()
        # in case of a "tie"
        if ans in itemList:
            rando = random.choice(itemList)
            if rando == ans:
                print ("|                       Computer chose same. Go again.                        |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                continue
            # in case of user win
            elif rando == itemList[0] and ans == itemList[1]:
                print ("|                            Computer chose \"" + itemList[0] + "\"                            |")
                print ("|                        You WIN this round (of three)                        |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                userWinCount += 1
                continue
            elif rando == itemList[2] and ans == itemList[0]:
                print ("|                            Computer chose \"" + itemList[2] + "\"                        |")
                print ("|                        You WIN this round (of three)                        |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                userWinCount += 1
                continue
            elif rando == itemList[1] and ans == itemList[2]:
                print ("|                            Computer chose \"" + itemList[1] + "\"                            |")
                print ("|                        You WIN this round (of three)                        |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                userWinCount += 1
                continue
            # in case of robo win
            elif ans == itemList[0] and rando == itemList[1]:
                print ("|                            Computer chose \"" + itemList[1] + "\"                           |")
                print ("|                        You LOSE this round (of three)                       |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                roboWinCount += 1
                continue
            elif ans == itemList[2] and rando == itemList[0]:
                print ("|                            Computer chose \"" + itemList[0] + "\"                            |")
                print ("|                        You LOSE this round (of three)                       |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                roboWinCount += 1
                continue
            elif ans == itemList[1] and rando == itemList[2]:
                print ("|                            Computer chose \"" + itemList[2] + "\"                        |")
                print ("|                        You LOSE this round (of three)                       |")
                print("+-----------------------------------------------------------------------------+")
                roundsPlayed += 1
                roboWinCount += 1
                continue
            break
        else:
            continue

# calculate final verdict of match
def getResult(userWinCount, roboWinCount, roundsPlayed):
    # if user won more times, user win
    if userWinCount > roboWinCount:
        print ("|                             You won: " + str(userWinCount) + " round(s)                             |")
        print ("|                           Computer won: " + str(roboWinCount) + " round(s)                          |")
        print ("|                            Rounds Played: " + str(roundsPlayed) + " rounds                          |")
        print("+-----------------------------------------------------------------------------+")
        return ("|        YOU  WIN ! ! !           |")
    # if robo won more times, robo win
    elif roboWinCount > userWinCount:
        print ("|                             You won: " + str(userWinCount) + " round(s)                             |")
        print ("|                           Computer won: " + str(roboWinCount) + " round(s)                          |")
        print ("|                            Rounds Played: " + str(roundsPlayed) + " rounds                          |")
        print("+-----------------------------------------------------------------------------+")
        return ("|              You  lose  :(              |")

# made for repeated game attempts
def retry(try_):
    print("+-----------------------------------------------------------------------------+")
    # sets up to retry if prompted "Yes"
    if try_ == "Yes":
        return 1
    # perform safe exit if prompted "No"
    elif try_ == "No":
        printy(fig.renderText("|    See you again    |"), "oB")
        sys.exit()

# driver
def main():
    gamesPlayed = 1
    gamesWon = 0
    gamesLost = 0
    # inifite loop to give users autonomy on how many games
    while True:
        if gamesPlayed == 1:
            graphic()
        else:
            printy(fig.renderText("|                Game " + str(gamesPlayed) + "                     |"), "pB")
        ready()
        if gamesPlayed == 1:
            printy(fig.renderText("|                Game     " + str(gamesPlayed) + "                     |"), "pB")
        chart()
        country = getCountry()
        getRules()
        itemList = getSpecificRules(country)
        ready2()
        userWinCount, roboWinCount, roundsPlayed = playGame(itemList)
        result = getResult(userWinCount, roboWinCount, roundsPlayed)
        if result.__contains__("WIN"):
            gamesWon += 1
            printy(fig.renderText(result), "nB")
            print("+-----------------------------------------------------------------------------+")
            print ("|                             You won: " + str(gamesWon) + " game(s).                             |")
            print ("|                           Computer won: " + str(gamesLost) + " game(s).                          |")
            print ("|                         Total Games Played: " + str(gamesPlayed) + " game(s)                       |")
            print("+-----------------------------------------------------------------------------+")
        else:
            gamesLost += 1
            printy(fig.renderText(result), "yB")
            print("+-----------------------------------------------------------------------------+")
            print ("|                             You won: " + str(gamesWon) + " game(s).                             |")
            print ("|                           Computer won: " + str(gamesLost) + " game(s).                          |")
            print ("|                         Total Games Played: " + str(gamesPlayed) + " game(s)                       |")
            print("+-----------------------------------------------------------------------------+")
        # prompt user to play again
        while True:
            try_ = input("|               Would you like to play again? (Yes/No) ").strip().title()
            if try_ == "Yes" or try_ == "No":
                break
        # call retry, continues through while loop if prompted "Yes"
        if retry(try_) == 1:
            gamesPlayed += 1
            continue

if __name__ == "__main__":
    main()
