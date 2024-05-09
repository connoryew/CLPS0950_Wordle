# This is the file that we will be using to write the code for our Wordle clone for the CLPS0950 Final Group Project
# Group Members: Nicole Chen, Jilienne Widener, Connor Yew

"""
Next Steps:
    - Put a "CLPS0950 Wordle" title at the top if we have room?
"""

import random
import pygame
import string

# Declaration of global color variables
GREEN = (0, 128, 0)
YELLOW = (255, 255, 0)
GRAY = (128, 128, 128)
LIGHTGRAY = (220, 220, 220)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# initalize the pygame game on load 
pygame.init()
screen = pygame.display.set_mode((550,700))
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
    window_width = screen.get_width()
    base_x = (window_width - (5*70))//2 
    base_y = 425 
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
    window_width = screen.get_width()
    base_x = (window_width - (5*70))//2
    for i, (guess, result) in enumerate(zip(guesses, results)):
        for j, (letter, res) in enumerate(zip(guess, result)):
            x = base_x + j * 70  # This positions each letter horizontally
            y = 50 + i * 70  # This positions each guess vertically
            color = GREEN if res == 'G' else YELLOW if res == 'Y' else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60))
            text_surface = base_font.render(letter, True, BLACK)
            letter_rect = text_surface.get_rect(center=(x + 30, y + 30))
            screen.blit(text_surface, letter_rect)

def draw_letter_bank(screen, key_colors):
    window_width = screen.get_width()
    rows = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ]
    base_y = 500
    max_width = max(len(row) * 50 for row in rows)
    for row_index, row in enumerate(rows):
        row_width = len(row) * 50
        base_x = (window_width - row_width) // 2
        for col_index, letter in enumerate(row):
            x = base_x + col_index * 50
            y = base_y + row_index * 50
            color = key_colors.get(letter, LIGHTGRAY)
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 40, 40))
            text_surface = base_font.render(letter, True, BLACK)
            letter_rect = text_surface.get_rect(center=(x + 20, y + 20))
            screen.blit(text_surface, letter_rect)

def update_letter_bank(guess,result,key_colors):
    for letter, res in zip(guess, result):
        if res == 'G':
            key_colors[letter] = GREEN
        elif res == 'Y':
            key_colors[letter] = YELLOW
        elif res == 'N' and key_colors[letter] not in [GREEN, YELLOW]:
            key_colors[letter] = GRAY

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
    key_colors = {letter: LIGHTGRAY for letter in string.ascii_uppercase}
    correct_guesses = set()
    background_color = "black"
    text_rect = pygame.Rect(50, 650, 400, 100)
    base_font = pygame.font.Font(None, 70)
    clock = pygame.time.Clock()
    isSubmitted = True


    while running:
        screen.fill(BLACK)  # Clear the screen at the start of each frame
        draw_guesses(screen, guesses, results)
        draw_underlines(screen, guess)  # Draw underlines for guess input
        draw_letter_bank(screen, key_colors)

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
                    if guess in guesses: 
                        message = f"You have already guessed that word. Try another."
                        pygame.display.set_caption(message)
                        continue

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
                        guesses_left -= 1
                        if guess_result == ['G'] * 5:
                            message = "Congratulations! You've guessed the word!"
                            game_over = True
                        elif guesses_left == 0:
                            message = f"Game over. The word was: {word}"  # Display message with the word
                            game_over = True
                        else:
                            message = "Keep Guessing!"
                        update_letter_bank(guess,guess_result,key_colors)
                        isSubmitted = True
                        pygame.display.set_caption(message)
                        guess = ""  # Reset guess after processing
                    else:
                        message = "Invalid input. Enter a valid 5-letter word."
                        pygame.display.set_caption(message)  # Display error message in window title
                else:
                    if len(guess) < 5 and event.unicode.isalpha() and not game_over:
                        guess += (event.unicode).upper()
                        window_width = screen.get_width()
                        base_x = (window_width- (5*70))//2
                        x = base_x + len(guess) *70 - 70
                        text_surface = base_font.render(guess[-1], True, WHITE)
                        screen.blit(text_surface, (x + 10, 700))
                        if guess[-1] in word:
                            if isSubmitted == False:
                                key_colors[guess[-1]] = GREEN
        if not game_over: 
            window_width = screen.get_width()
            base_x = (window_width - (5*70))//2
            base_y = 425
            for i, letter in enumerate(guess):
                x = base_x + i * 70
                text_surface = base_font.render(letter, True, WHITE)
                screen.blit(text_surface, (x+10, base_y))  # Position the text entry near the bottom

        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == '__main__':
    WordleClone()