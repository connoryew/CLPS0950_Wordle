# CLPS0950 Wordle Clone Project
# Group Members: Nicole Chen, Jilienne Widener, Connor Yew

# Imports our modules, which helps us to pick a random word (random), run the game interface (pygame), and access a set of ASCII uppercase letters (string)
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

# Initalizes our pygame game window on load 
pygame.init()
screen = pygame.display.set_mode((550,730)) # This line sets the dimensions for the window (width, length)
pygame.display.set_caption("Wordle Clone")
base_font = pygame.font.Font(None, 70)
clock = pygame.time.Clock()


def load_words():
    """Assigns a list of 5-letter Wordle words from the wordlist.txt file to the variable "words" """
    with open ('wordlist.txt', 'r') as file: 
        words = [line.strip().upper() for line in file if len(line.strip())== 5]
        return words

def load_guesses():
    """ Assigns a list of 5-letter possible Wordle guesses from the possibleguesses.txt file to the variable "words" """
    with open('possibleguesses.txt', 'r') as file:
        words = [line.strip().upper() for line in file if len(line.strip())== 5]
        return words

def generate_word():
    """ Selects a random word from the 5-letter word list made by load_words """
    words = load_words() 
    return random.choice(words)

def draw_underlines(screen, guess):
    """ 
    Takes screen width and guess length into account to draw 5 grey, centered underlines
    that are replaced with white underlines as the player writes in their guesses 
    """
    window_width = screen.get_width()
    base_x = (window_width - (5*70))//2 # Centers the underlines within the window width
    base_y = 485 # Sets the fixed height at which the underlines will be drawn 
    for i in range(5):  # Draws 5 underlines
        x = base_x + i * 70  # Position each underline
        if i < len(guess):
            pygame.draw.line(screen, WHITE, (x, base_y + 50), (x + 50, base_y + 50), 2)  # Draws a solid, white underline if a letter is types
        else:
            pygame.draw.line(screen, GRAY, (x, base_y + 50), (x + 50, base_y + 50), 2)  # Draws a fainter, grey underline if a letter is not typed

def check_guess(word, guess):
    """ Determines the accuracy of the player's guess in comparison to the random target word """
    validity = ['N'] * 5 # Initializes accuracy to 'N' for GRAY
    word_count = {}
    for letter in word: 
        if letter in word_count: 
            word_count[letter] += 1
        else: 
            word_count[letter] = 1

    # Marks correctly placed letters within the player's guess as 'G' for GREEN by comparing the position of each letter in guess to each letter in word
    for i in range(len(guess)): 
        if guess[i] == word[i]:
            validity[i] = 'G'
            word_count[guess[i]] -= 1

    # Marks incorrectly placed correct letters within the player's guess as 'Y' for YELLOW by making sure the letter isn't green but is still found in word 
    for i in range(len(guess)):
        if guess[i] != word[i] and guess [i] in word and word_count[guess[i]] > 0: 
            validity[i] = 'Y' 
            word_count[guess[i]] -= 1 

    return validity 

def draw_guesses(screen, guesses, results):
    """Draws the guesses with the validity-based color coding from check_guess on the pygame screen."""
    window_width = screen.get_width()
    base_x = (window_width - (5*70))//2
    for i, (guess, result) in enumerate(zip(guesses, results)): # Outer loop pairs each guess with its result
        for j, (letter, res) in enumerate(zip(guess, result)): # Inner loop pairs each letter within a guess with its validity
            x = base_x + j * 70  # This positions each letter horizontally
            y = 80 + i * 70  # This positions each guess vertically
            color = GREEN if res == 'G' else YELLOW if res == 'Y' else GRAY
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 60, 60)) # Draws the appropriately-colored squares and letters for each guess once it has been submitted
            text_surface = base_font.render(letter, True, BLACK)
            letter_rect = text_surface.get_rect(center=(x + 30, y + 30))
            screen.blit(text_surface, letter_rect)

def update_letter_bank(guess,result,key_colors):
    """ 
    Creates a dictionary of validity-based color assignments for each 
    letter that will be used to update the letter bank after each guess
    """
    for letter, res in zip(guess, result): # Iterates through each letter in a player's guess and pairs each letter with its validity
        if res == 'G':
            key_colors[letter] = GREEN
        elif res == 'Y':
            key_colors[letter] = YELLOW
        elif res == 'N' and key_colors[letter] not in [GREEN, YELLOW]:
            key_colors[letter] = GRAY

def draw_letter_bank(screen, key_colors):
    """ Draws a letter bank in QWERTY formatting to allow the player to track which leters have already been correctly guessed or eliminated """
    window_width = screen.get_width()
    rows = [
        "QWERTYUIOP",
        "ASDFGHJKL",
        "ZXCVBNM"
    ]
    base_y = 565 # Sets the fixed height at which the letter bank will be drawn
    letter_bank_font = pygame.font.Font(None, 60)  # NOTE: Reduced from base_font, which was at 70

    max_width = max(len(row) * 50 for row in rows) # Calculates the width needed to fit each row of letters in the letter bank
    for row_index, row in enumerate(rows):
        row_width = len(row) * 50
        base_x = (window_width - row_width) // 2 # Centers each row of letters in the window
        for col_index, letter in enumerate(row): # Positions each letter in the correct position with the appropriately-colored boxes
            x = base_x + col_index * 50
            y = base_y + row_index * 50
            color = key_colors.get(letter, LIGHTGRAY) # Retrieves the color assignments for each letter and sets all unassigned letters to LIGHTGRAY
            pygame.draw.rect(screen, color, pygame.Rect(x, y, 40, 40)) # Draws the boxes for each letter in the letter bank
            text_surface = letter_bank_font.render(letter, True, BLACK)
            letter_rect = text_surface.get_rect(center=(x + 20, y + 20))
            screen.blit(text_surface, letter_rect)

def WordleClone():
    """ Runs our Wordle gameplay loop """

    # INITIALIZATION:
    word = generate_word()
    print(f'For testing, the word is {word}') # NOTE: Comment out this line once your code is finished to avoid giving the answer away to players
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
    title_font = pygame.font.Font(None, 75)  # NOTE: Increased from base_font, which was at 70
    clock = pygame.time.Clock() # Creates a pygame clock object, which can be used to control the frame rate of the game
    isSubmitted = True


    while running:
        screen.fill(BLACK)  # Clears the screen at the start of each frame
       

        # Displays the "CLPS0950WORDLE" title at the top
        title_surface = title_font.render("CLPS0950 Wordle", True, WHITE)
        title_rect = title_surface.get_rect(center=(screen.get_width() // 2, 40))
        screen.blit(title_surface, title_rect)

        # Renders in the the letter bank, the underlines the guesses will be written on, and the player's guesses
        draw_guesses(screen, guesses, results)
        draw_underlines(screen, guess)  # Draws underlines for guess input
        draw_letter_bank(screen, key_colors)
        draw_guesses(screen, guesses, results)
        draw_underlines(screen, guess)  # Draws underlines for guess input
        draw_letter_bank(screen, key_colors)

        # EVENT LOOP:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # Allows players to end the game by quitting
                running = False
            
            if game_over: # Skips the rest of the loop early if the game has ended
                continue

            if guesses_left == 0 or not running:
                message = f"Game over. The word was: {word}"
                pygame.display.set_caption(message)  # Displays the end game message in window title
                game_over = True

            if event.type == pygame.KEYDOWN: # Detects player's key inputs and allows them to type in, delete, and submit guesses
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
                            message = f"Game over. The word was: {word}"  # Displays the game over message with the correct word
                            game_over = True
                        else:
                            message = "Keep Guessing!"
                        update_letter_bank(guess,guess_result,key_colors)
                        isSubmitted = True
                        pygame.display.set_caption(message)
                        guess = ""  # Resets guess after processing whether the guess was correct or not
                    else:
                        message = "Invalid input. Enter a valid 5-letter word."
                        pygame.display.set_caption(message)  # Displays the error message in window title when a player inputs a string that isn't a valid 5-letter word
                else:
                    if len(guess) < 5 and event.unicode.isalpha() and not game_over: # Updates and displays the guess as the player is writing it
                        guess += (event.unicode).upper()
                        window_width = screen.get_width()
                        base_x = (window_width- (5*70))//2
                        x = base_x + len(guess) *70 - 70
                        text_surface = base_font.render(guess[-1], True, WHITE)
                        screen.blit(text_surface, (x + 10, 700))
                        if guess[-1] in word:
                            if isSubmitted == False:
                                key_colors[guess[-1]] = GREEN

        if not game_over: # Renders the submitted guess on the screen with the appropriately colored letters as long as the game hasn't ended yet
            window_width = screen.get_width()
            base_x = (window_width - (5*70))//2
            base_y = 485
            for i, letter in enumerate(guess):
                x = base_x + i * 70
                text_surface = base_font.render(letter, True, WHITE)
                screen.blit(text_surface, (x+10, base_y))  # Positions the text entry near the bottom

        pygame.display.flip() # Updates the entire pygame display
        clock.tick(60) # Sets our game's frame rate to 60 frames/second

    pygame.quit()

if __name__ == '__main__':
    WordleClone()