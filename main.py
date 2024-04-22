import pygame
import sys
import random


from welcome_screen import show_welcome_screen


pygame.init()
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))

# Show the welcome screen
show_welcome_screen(screen)


# Initialize Pygame
pygame.init()

# window setup
screen_width = 1000
screen_height = 800
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption('Wordle Game')

# wordle main colors
white = (255, 255, 255)
black = (0, 0, 0)
gray = (120,124,127)
green = (108,169,101)
yellow = (200,182,83)
lightgray = (211, 211, 211)

# basic setup
clock = pygame.time.Clock()
font = pygame.font.Font(None, 64)

title_font = pygame.font.SysFont('Georgia', 48, bold=True)

key_feedback = {letter: white for letter in "QWERTYUIOPASDFGHJKLZXCVBNM"}
guess_font = pygame.font.SysFont('Franklin Gothic', 36)



# confetti for when player wins the game
class Confetti:
    def __init__(self, screen_width, screen_height):
        self.x = random.randint(0, screen_width)
        self.y = random.randint(-screen_height, 0)
        self.size = random.randint(3, 8)
        self.color = random.choice([(168, 100, 253), (41, 205, 255), (120, 255, 68), (255, 113, 141), (253, 255, 106)])
        self.fall_speed = random.randint(2, 5)
        self.x_speed = random.choice([-1, 1]) * random.random() * 2

    def fall(self):
        self.y += self.fall_speed
        self.x += self.x_speed
        self.x += 0.5 if random.randint(0, 10) > 5 else -0.5

        # reset if needed
        if self.y > screen_height:
            self.y = random.randint(-100, 0)
            self.x = random.randint(0, screen_width)

    def draw(self, screen):
        pygame.draw.circle(screen, self.color, (int(self.x), int(self.y)), self.size)

confetti = []
celebration = False


def draw_title(screen, title, font, y_offset=20):
    text_surface = font.render(title, True, black)
    x_centered = (screen_width - text_surface.get_width()) // 2
    screen.blit(text_surface, (x_centered, y_offset))



# func to load words from file and get one randomly
def load_words(filename):
    with open(filename, 'r') as file:
        words = file.read().splitlines()  # read the file and split into lines
    return words

# load valid words from file
all_words = load_words('wordle_answers.txt')
word = random.choice(all_words)
word_split = [*word]

print(f"The selected word is: {word}")  # just for debugging so we can see what the word is

# func to draw the  grid and color letters based on feedback
def draw_grid(screen, guesses, feedback, grid_size=(5, 6), cell_size=55, cell_margin=15):
    grid_width, grid_height = grid_size
    start_x = (screen_width - (grid_width * (cell_size + cell_margin) - cell_margin)) // 2
    start_y = (screen_height - (grid_height * (cell_size + cell_margin) - cell_margin)) // 4

    # define initial colors
    border_color_initial = gray
    fill_color_initial = white
    text_color_initial = black

    for row in range(grid_height):
        for col in range(grid_width):
            x = start_x + col * (cell_size + cell_margin)
            y = start_y + row * (cell_size + cell_margin)
            cell_rect = pygame.Rect(x, y, cell_size, cell_size)

            # draw each cell with a gray border and white fill
            pygame.draw.rect(screen, fill_color_initial, cell_rect)  # fill cell with white
            pygame.draw.rect(screen, border_color_initial, cell_rect, 3)  # gray border

            # define text color based on whether a guess has been made
            text_color = text_color_initial
            feedback_color = fill_color_initial

            if row < len(guesses) and col < len(guesses[row]):
                letter = guesses[row][col].upper()
                # if feedback, then update text color to white and fill/border color to feedback color
                if row < len(feedback) and col < len(feedback[row]):
                    feedback_color = feedback[row][col]
                    text_color = white
                    pygame.draw.rect(screen, feedback_color, cell_rect)  # update fill to feedback color
                    pygame.draw.rect(screen, feedback_color, cell_rect, 3)  # update border to the same color


                text_surface = font.render(letter, True, text_color)
                screen.blit(text_surface, (x + (cell_size - text_surface.get_width()) // 2, y + (cell_size - text_surface.get_height()) // 2))


def draw_reset_button(screen, font):
    button_color = (211, 211, 211)

    text_color = black
    button_rect = pygame.Rect(screen_width - 950, screen_height - 770, 100, 40)

    button_font = pygame.font.SysFont('Georgia', 30) # changed font to Georgia (closer to real game)

    pygame.draw.rect(screen, button_color, button_rect)  # draw reset button

    text_surface = button_font.render('Reset', True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

    return button_rect

def draw_guess_button(screen, font):
    button_color = green

    text_color = white
    button_rect = pygame.Rect(screen_width / 2 - 85, screen_height / 2 + 110, 170, 50)

    button_font = pygame.font.SysFont('Georgia', 20) 

    pygame.draw.rect(screen, button_color, button_rect)

    text_surface = button_font.render('Solver', True, text_color)
    text_rect = text_surface.get_rect(center=button_rect.center)

    screen.blit(text_surface, text_rect)

    return button_rect


# find feedback for a guess
def generate_feedback(guess):
    feedback = []
    for i, letter in enumerate(guess):
        if word_split[i] == letter:
            feedback.append(green)  # right letter and position
        elif letter in word_split:
            feedback.append(yellow)  # right letter, wrong position
        else:
            feedback.append(gray)  # letter not in word
    return feedback

def draw_keyboard(screen, key_feedback, font):
    light_gray = (211, 211, 211)  # light gray

    key_width = 60
    key_height = 60
    key_margin = 10
    corner_radius = 10  # rounded corners

    # define the keyboard rows
    keyboard_rows = ["QWERTYUIOP", "ASDFGHJKL", "ZXCVBNM"]

    # find starting x position to center the keyboard
    total_keys_width = max([len(row) for row in keyboard_rows]) * (key_width + key_margin) - key_margin
    start_x = (screen_width - total_keys_width) // 2

    # Start y position for the keyboard
    start_y = screen_height - (3 * key_height) - (2 * key_margin) - 20

    for i, row in enumerate(keyboard_rows):
        row_width = len(row) * (key_width + key_margin) - key_margin
        row_start_x = start_x + (total_keys_width - row_width) // 2

        for j, key in enumerate(row):
            key_x = row_start_x + j * (key_width + key_margin)
            key_y = start_y + i * (key_height + key_margin)


            pygame.draw.rect(screen, light_gray, [key_x, key_y, key_width, key_height], border_radius=corner_radius)


            text_surface = font.render(key, True, black)
            text_x = key_x + (key_width - text_surface.get_width()) // 2
            text_y = key_y + (key_height - text_surface.get_height()) // 2
            screen.blit(text_surface, (text_x, text_y))


def draw_popup_message(screen, message, font, background_color, text_color, duration=2):

    text_surface = font.render(message, True, text_color)
    text_rect = text_surface.get_rect(center=(screen_width // 2, screen_height // 2))

    background_rect = text_rect.inflate(20, 10)
    pygame.draw.rect(screen, background_color, background_rect)
    screen.blit(text_surface, text_rect)

    pygame.display.update(background_rect)
    pygame.time.wait(duration * 1000)

def draw_back_button(screen):
    button_color = (211, 211, 211)  # light gray
    text_color = (0, 0, 0)
    button_font = pygame.font.SysFont('Georgia', 30)
    button_text = "Back"
    button_rect = pygame.Rect(50, screen_height - 715, 100, 40)

    # draw the button rectangle
    pygame.draw.rect(screen, button_color, button_rect)

    # draw the button text
    text_surf = button_font.render(button_text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect

def draw_hint_button(screen):
    button_color = (211, 211, 211)
    text_color = black
    button_font = pygame.font.SysFont('Georgia', 30)
    button_text = "Hint"
    button_rect = pygame.Rect(screen_width - 150, screen_height - 770, 100, 40)

    # button rectangle
    pygame.draw.rect(screen, button_color, button_rect)

    # button text
    text_surf = button_font.render(button_text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect


def draw_solver_button(screen):
    button_color = (211, 211, 211)
    text_color = black
    button_font = pygame.font.SysFont('Georgia', 30)
    button_text = "Solve"
    button_rect = pygame.Rect(screen_width - 150, screen_height - 715, 100, 40)

    pygame.draw.rect(screen, button_color, button_rect)

    text_surf = button_font.render(button_text, True, text_color)
    text_rect = text_surf.get_rect(center=button_rect.center)
    screen.blit(text_surf, text_rect)

    return button_rect



# main game loop
running = True
current_guess = ""
guesses = []
feedback = []
back_button_rect = draw_back_button(screen)





while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RETURN and len(current_guess) == 5:
                # check if the guess is in the list of words
                if current_guess in all_words:
                    feedback_color = generate_feedback(current_guess)  # feedback for the current guess
                    guesses.append(current_guess)
                    feedback.append(feedback_color)
                    if all(color == green for color in feedback_color):  # check if all letters are green (correct guess)
                        celebration = True
                        confetti = [Confetti(screen_width, screen_height) for _ in range(200)]  # make 200 pieces of confetti
                    current_guess = ""  # reset for next guess
                else:
                    # popup that word is not in list
                    draw_popup_message(screen, "Not a valid word", font, (211, 211, 211), (0, 0, 0))
                    pygame.display.flip()
                    pygame.time.wait(2000)  # wait for 2 seconds to show the message ( might change this)


            elif event.key == pygame.K_BACKSPACE:
                current_guess = current_guess[:-1]  # remove last letter
            elif len(current_guess) < 5 and event.unicode.isalpha():
                current_guess += event.unicode.lower()  # add new letter
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = event.pos
            if button_rect.collidepoint(mouse_pos):
                # reset game
                guesses = []  # reset guesses list
                feedback = []  # reset feedback list
                current_guess = ""
                celebration = False
                confetti = []
            if event.type == pygame.MOUSEBUTTONDOWN:
                if back_button_rect.collidepoint(event.pos):
                    show_welcome_screen(screen)


    screen.fill(white)
    draw_title(screen, "Wordle", title_font)
    button_rect = draw_reset_button(screen, font)
    guess_button = draw_guess_button(screen, font)
    draw_keyboard(screen, key_feedback, guess_font)
    draw_grid(screen, guesses + [current_guess] if current_guess else guesses, feedback)
    back_button_rect = draw_back_button(screen)
    hint_button_rect = draw_hint_button(screen)
    solver_button_rect = draw_solver_button(screen)

    # draw the confetti is celebrtion true
    if celebration:
        for piece in confetti:
            piece.fall()
            piece.draw(screen)


    pygame.display.flip()
    clock.tick(60)

pygame.quit()