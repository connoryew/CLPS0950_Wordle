# This is the file that we will be using to write the code for our Wordle clone for the CLPS0950 Final Group Project
# Group Members: Nicole Chen, Jilienne Widener, Connor Yew

import random
import pygame

def load_words(): 
    # This function loads a list of 5-letter words from a file
    with open ('wordlist.txt', 'r') as file: 
        words = [line.strip().upper() for line in file if len(line.strip())== 5]
        return words
    

def load_guesses():
    with open('possibleguesses.txt', 'r') as file:
        words = [line.strip().upper() for line in file if len(line.strip())== 5]
        return words
    
def generate_word():
    # This function selects a random word from the list 
    words = load_words() 
    return random.choice(words)

def check_guess(word, guess):
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
    # Init wordle 
    word = generate_word()
    print(f'For testing, the word is {word}')
    possible_guesses = load_guesses()
    # print(f'The possible guesses are {possible_guesses}')
    
    guesses_left = 6 
    has_won = False 
    isPossibleGuess = False

    guess = ''

    # Init pygame
    pygame.init()
    screen = pygame.display.set_mode((500,800))
    background_color = "black"
    text_rect = pygame.Rect(50, 650, 400, 100)
    base_font = pygame.font.Font(None, 70)
    clock = pygame.time.Clock()
    running = True

    guesses = []

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if guesses_left == 0:
                print("Game over. The word was:", word)

            # check if user types
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN:
                    if len(guess) != 5:
                        print(f"Invalid input. {guess} is not a valid guess. Please enter a 5-letter word.")
                        continue

                    if not guess.isalpha():
                        print(f"Invalid input. {guess} is not a valid guess. Please enter only letters.")
                        continue

                    if not guess in possible_guesses:
                        print(f"Invalid input. {guess} is not a valid guess. Please enter a real word.")
                        continue 

                    # Process Guess 
                    result = check_guess(word,guess)
                    print(f"Guessed <{guess}> for word <{word}>")
                    print(' '.join(result))

                    guesses.append(guess)
                    guess = ""

                    guesses_left -= 1
                    print(f'Guesses left: {guesses_left}')

                    if result == ['G', 'G', 'G', 'G', 'G']:
                        print("Congratulations! You've guessed the word!")
                        has_won = True
                        break
                else:
                    if len(guess) < 5:
                        guess += (event.unicode).upper()

        
        screen.fill(background_color)
        pygame.draw.rect(screen, "white", text_rect)

        for i, past_guess in enumerate(guesses):
            x = 50
            y = 20 + i * 100
            result = result(past_guess)
            pygame.draw.rect(screen, "white", pygame.Rect(x, y, 400, 80))
            text_surface = base_font.render(past_guess, True, "black")
            screen.blit(text_surface, (x + 5, y + 5))


            

        text_surface = base_font.render(guess, True, "black")
        screen.blit(text_surface, (text_rect.x + 5, text_rect.y + 5))

        pygame.display.flip()

        clock.tick(60)


    pygame.quit()

    # while guesses_left > 0: 
    #     guess = input('Enter your guess: ').upper().strip()

    #     if len(guess) != 5:
    #         print(f"Invalid input. {guess} is not a valid guess. Please enter a 5-letter word.")
    #         continue

    #     if not guess.isalpha():
    #         print(f"Invalid input. {guess} is not a valid guess. Please enter only letters.")
    #         continue

    #     if guess in possible_guesses:
    #         isPossibleGuess = True
            

    #     if isPossibleGuess == False:
    #         print(f"Invalid input. {guess} is not a valid guess. Please enter a real word.")
    #         continue 

    #     if isPossibleGuess == True:
    #         print(f'You guessed {guess}')

    #     # Process Guess 
    #     result = check_guess(word,guess)
    #     print(' '.join(result))
    #     guesses_left -= 1
    #     print(f'Guesses left: {guesses_left}')
    #     isPossibleGuess = False

    #     if result == ['G', 'G', 'G', 'G', 'G']:
    #         print("Congratulations! You've guessed the word!")
    #         has_won = True
    #         break

    # if not has_won:
    #     print("Game over. The word was:", word)

    

if __name__ == '__main__':
    WordleClone()
