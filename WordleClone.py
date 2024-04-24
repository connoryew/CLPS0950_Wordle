# This is the file that we will be using to write the code for our Wordle clone for the CLPS0950 Final Group Project
# Group Members: Nicole Chen, Jilienne Widener, Connor Yew

import random

def load_words(): 
    # This function loads a list of 5-letter words from a file
    with open ('wordlist.txt', 'r') as file: 
        words = [line.strip().upper() for line in file if len(line.strip())== 5]
        return words 
    
def generate_word():
    # This function selects a random word from the list 
    words = load_words() 
    return random.choice(words)

def check_guess(word, guess):
    print(f'For testing, the word is {word}')
    validity = ['N'] * 5 # Defaults all to 'N'
    word_count = {}
    for letter in word: 
        if letter in word_count: 
            word_count[letter] += 1
        else: 
            word_count[letter] = 1

    # Marks Correct Placements 
    for i in range(len(guess)): 
        if guess[i] == word[i]:
            validity[i] = 'G'
            word_count[guess[i]] -= 1

    # Marks Correct Letters in Wrong Positions 
    for i in range(len(guess)):
        if guess[i] != word[i] and guess [i] in word and word_count[guess[i]] > 0: 
            validity[i] = 'Y' 
            word_count[guess[i]] -= 1 

    return validity 
 
def WordleClone():
    word = generate_word()

    guesses_left = 6 
    has_won = False 

    while guesses_left > 0: 
        guess = input('Enter your guess: ').upper().strip()

        # Validate Input 
        if len(guess) != 5 or not guess.isalpha(): 
            print("Invalid input. Please enter a 5-letter word,")
            continue 

        # Process Guess 
        result = check_guess(word,guess)
        print(' '.join(result))
        guesses_left -= 1
        print(f'Guesses left: {guesses_left}')

        if result == ['G', 'G', 'G', 'G', 'G']:
            print("Congratulations! You've guessed the word!")
            has_won = True
            break

    if not has_won:
        print("Game over. The word was:", word)

if __name__ == '__main__':
    WordleClone()


#currently it doesn't generate a random word i.e. requires target word input, 
#doesn't tell you if word does not exist or if it's repeated 
#doesn't check if the word being typed is >5 words (doesn't stop you from doing so)
#only want one letter/color (G,Y,N) to show up for repeated letters
#need game ends/breaks
