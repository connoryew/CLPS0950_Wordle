# This is the file that we will be using to write the code for our Wordle clone for the CLPS0950 Final Group Project
# Group Members: Nicole Chen, Jilienne Widener, Connor Yew

import random
import pygame

# Declaration of global color variables
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# initalize the pygame game on load 
pygame.init()
screen = pygame.display.set_mode((500,800))
pygame.display.set_caption("Wordle Clone")
base_font = pygame.font.Font(None, 70)
clock = pygame.time.Clock()


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

def draw_underlines(screen, guess):
    """Draws underlines for each letter in the guess area."""
    base_x, base_y = 50, 700  # Starting position for the underlines
    for i in range(5):  # Draw 5 underlines
        x = base_x + i * 70  # Position each underline
        if i < len(guess):
            pygame.draw.line(screen, WHITE, (x, base_y + 50), (x + 50, base_y + 50), 2)  # Draw solid underline for typed letters
        else:
            pygame.draw.line(screen, GRAY, (x, base_y + 50), (x + 50, base_y + 50), 2)  # Draw faint underline for empty slots


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


def draw_guesses(screen, guesses, results):
    """Draws the guesses with color coding on the Pygame screen."""
    for i, (guess, result) in enumerate(zip(guesses, results)):
        for j, (letter, res) in enumerate(zip(guess, result)):
            x = 50 + j * 70  # This positions each letter horizontally
            y = 50 + i * 70  # This positions each guess vertically
            color = GREEN if res == 'G' else YELLOW if res == 'Y' else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
            text_surface = base_font.render(letter, True, BLACK)
            letter_rect = text_surface.get_rect(center=(x + 30, y + 30))
            screen.blit(text_surface, letter_rect)

 
def WordleClone():
    # Init wordle 
    word = generate_word()
    print(f'For testing, the word is {word}')
    possible_guesses = load_guesses()
    guesses = []
    results = []
    guess = ''
    
    guesses_left = 6 
    isPossibleGuess = False
    running = True 
    game_over = False 
    background_color = "black"
    text_rect = pygame.Rect(50, 650, 400, 100)
    base_font = pygame.font.Font(None, 70)
    clock = pygame.time.Clock()


    while running:
        screen.fill(BLACK)  # Clear the screen at the start of each frame
        draw_guesses(screen, guesses, results)
        draw_underlines(screen, guess)  # Draw underlines for guess input

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if game_over:
                continue

            if guesses_left == 0 or not running:
                message = f"Game over. The word was: {word}"
                pygame.display.set_caption(message)  # Display end game message in window title
                # pygame.time.wait(3000)  # Wait for 3 seconds before closing
                game_over = True

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE and not game_over:
                    guess = guess[:-1]
                elif event.key == pygame.K_RETURN and not game_over:

                    if len(guess) != 5:
                        message = f"Invalid input. {guess} is not a valid guess. Please enter a 5-letter word."
                        pygame.display.set_caption(message)
                        continue
                    if not guess.isalpha():
                        message = f"Invalid input. {guess} is not a valid guess. Please enter only letters."
                        pygame.display.set_caption(message)
                        continue
                    
                    if not guess in possible_guesses:
                        message = f"Invalid input. {guess} is not a valid guess. Please enter a real word."
                        pygame.display.set_caption(message)
                        continue

                    if len(guess) == 5 and guess.isalpha() and guess in possible_guesses:
                        guess_result = check_guess(word, guess)
                        guesses.append(guess)
                        results.append(guess_result)
                        guess = ""
                        guesses_left -= 1
                        message = "Keep Guessing!"
                        pygame.display.set_caption(message)  # Display error message in window title
                        if guess_result == ['G'] * 5:
                            message = "Congratulations! You've guessed the word!"
                            pygame.display.set_caption(message)  # Display success message in window title
                            results[-1] = ['G'] * 5
                            draw_guesses(screen, guesses, results)
                            game_over = True
                        elif guesses_left ==0:
                            game_over = True
                    else:
                        message = "Invalid input. Enter a valid 5-letter word."
                        pygame.display.set_caption(message)  # Display error message in window title
                else:
                    if len(guess) < 5 and event.unicode.isalpha() and not game_over:
                        guess += (event.unicode).upper()
        if not game_over: 
            base_x, base_y = 50, 700
            for i, letter in enumerate(guess):
                x = base_x + i * 70
                text_surface = base_font.render(letter, True, WHITE)
                screen.blit(text_surface, (x+10, base_y))  # Position the text entry near the bottom


        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    WordleClone()