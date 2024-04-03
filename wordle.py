#splits up the word
word = "erase"
word_split = [*word]

#opens up the file with valid words and reads them all in lowercase
file = open('wordle.txt',"r")
valid_words = (file.read()).lower()

#checks if word is in the word list, returns true if the word is a valid word
def correct(word):
    found = valid_words.find(word)
    if (len(word) == 5):
        if found != -1:
            return True
        else:
            print("The word is not a valid word. Try again.")
            return False
    elif(len(word)>5):
        print("The word is too long. Try again.")
        return False
    else:
        print("The word is too short. Try again.")
        return False

#feedback on guess
def feedback(round):
    print()
    user = str(input("What is your word guess? : "))

    if correct(user):
        current = [*user] 
        results = ["b"]*5

        print(f"your guess was {current}")
        round = round + 1

        #checks if the letter in right position and adds to greenlist
        for i in range(5):
            if(word_split[i] == current[i]):
                greenlist[i] = current[i]
                results[i] = "g"

        #checking yellows
        for x in range(5):
            if greenlist[x] == current[x]:
                #skips if the current letter is in the greenlist(therefore in word and correct position)
                break
            elif ((current[x] in word_split) and (current[x] != word_split[x])) and (greenlist.count(current[x]) != word_split.count(current[x])) and (yellowlist.count(current[x]) + greenlist.count(current[x]) != word_split.count(current[x])):
                yellowlist[x]=(current[x])
                results[x] = "y"
            else:
                print(f"{current[x]} in index {x} is not in the word")
        

        #adding to blacklist -> letter not in yellow
        for x in range(5):
            if current[x] not in greenlist and current[x] not in yellowlist:
                blacklist[x] = current[x]

        print(f"Your results were {results}")
        return user,round
    
    else:
        feedback(round)
    
print("Welcome to Wordle\n")

for round in range(1,7):

    #set up variables
    greenlist = [""]*5
    yellowlist = [""]*5
    blacklist = [""]*5

    #check how the word did
    result = feedback(round)
    
    #return results
    print(f"green -> {greenlist}")
    print(f"yellow -> {yellowlist}")
    print(f"black -> {blacklist}")

    #check if word correct
    if(result == True):
        print(f"Congrats, you have gotten the word correct! You got it correct on round {round}")
        break
    
    #check if the amount of rounds is up
    if(round == 6):
        print(f"You have not gotten the correct word. The word is {word}")
        break
