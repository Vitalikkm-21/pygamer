import pygame
import random
import pygame.freetype
import pygame.mixer
import time

# Initialize Pygame
pygame.init()

# Set up some constants
WIDTH, HEIGHT = 1080, 1080
BACKGROUND_COLOR = (255, 255, 255)
FONT_COLOR = (0, 0, 0)
FONT_SIZE = 32
MARGIN = 20
ANIMATION_DELAY = 30  # Slow down the animation by three times
MUSIC_SPEED = 1  # Adjust music speed

# Fonts and button settings
FONT = pygame.font.Font(None, FONT_SIZE)
BUTTON_SIZE = (100, 50)
BUTTON_COLOR = (0, 128, 0)
BUTTON_FONT_COLOR = (255, 255, 255)
BUTTON_FONT_COLOR_red = (255, 0, 0)
BUTTON_FONT_COLOR_green = (0, 255, 0)
BUTTON_FONT_COLOR_blue = (0, 0, 255)
BUTTON_FONT = pygame.font.Font(None, 20)

# Set up variables
flips = 0
heads = 0
tails = 0
flip_result = ""
animation_frames = {"heads": [], "tails": []}
current_frame = 0
typing = False
text = ''
text_surface = None
ball = 0
mistake = 0
goal = -1
animation_finished = False

# Create the screen
screen = pygame.display.set_mode((WIDTH, HEIGHT))

# Create the flip button
flip_button = pygame.Rect(MARGIN, MARGIN, BUTTON_SIZE[0], BUTTON_SIZE[1])
flip_text = BUTTON_FONT.render("Flip", True, BUTTON_FONT_COLOR)

# Create buttons for different levels and exit
exit_button = pygame.Rect(WIDTH - MARGIN - BUTTON_SIZE[0], MARGIN, BUTTON_SIZE[0], BUTTON_SIZE[1])
exit_text = BUTTON_FONT.render("Exit", True, BUTTON_FONT_COLOR)

level_button_1 = pygame.Rect(WIDTH - MARGIN - BUTTON_SIZE[0] - 100, MARGIN, BUTTON_SIZE[0], BUTTON_SIZE[1])
level_text_1 = BUTTON_FONT.render("Level_1", True, BUTTON_FONT_COLOR)

level_button_2 = pygame.Rect(WIDTH - MARGIN - BUTTON_SIZE[0] - 200 , MARGIN, BUTTON_SIZE[0], BUTTON_SIZE[1])
level_text_2 = BUTTON_FONT.render("Level_2", True, BUTTON_FONT_COLOR)

level_button_3 = pygame.Rect(WIDTH - MARGIN - BUTTON_SIZE[0] - 300, MARGIN, BUTTON_SIZE[0], BUTTON_SIZE[1])
level_text_3 = BUTTON_FONT.render("Level_3", True, BUTTON_FONT_COLOR)

# Load sound
flip_sound = pygame.mixer.Sound("flip_sound.mp3")
flip_sound.set_volume(MUSIC_SPEED)

flip_sound_2 = pygame.mixer.Sound("Орел.mp3")
flip_sound_3 = pygame.mixer.Sound("Решка.mp3")
flip_sound_4 = pygame.mixer.Sound("bakh-tokkata-bwv-565.mp3")

# Function to load animation frames
def load_animation_frames(file_name_prefix, num_frames):
    frames = []
    for i in range(num_frames):
        if i <= 9:
            frame = pygame.image.load(file_name_prefix + "/" + file_name_prefix + "00" + str(i) + ".png")
        elif i <= 99:
            frame = pygame.image.load(file_name_prefix + "/" + file_name_prefix + "0" + str(i) + ".png")
        else:
            frame = pygame.image.load(file_name_prefix + "/" + file_name_prefix + str(i) + ".png")
        frames.append(frame)
    return frames

# Load the animation frames
animation_frames["heads"] = load_animation_frames("heads", 115)
animation_frames["tails"] = load_animation_frames("tails", 115)

# Function to draw the animation
def draw_animation():
    global current_frame, flip_result, animation_finished

    if not animation_finished:
        if flip_result not in animation_frames:
            flip_result = 'heads'
        if flip_result == 'heads':
            frame = animation_frames['heads'][current_frame]
        else:
            frame = animation_frames['tails'][current_frame]
        screen.blit(frame, (WIDTH / 2 - frame.get_width() / 2 + 350, HEIGHT / 2 - frame.get_height() / 2 - 250))
        current_frame += 1
        if current_frame >= len(animation_frames[flip_result]):
            animation_finished = True
            if flip_result == 'heads':
                flip_sound_3.play()
            else:
                flip_sound_2.play()

# Function to draw the buttons
def draw_buttons():
    pygame.draw.rect(screen, BUTTON_COLOR, exit_button)
    screen.blit(exit_text, (exit_button.x + (exit_button.width / 2) - (exit_text.get_width() / 2),
                            exit_button.y + (exit_button.height / 2) - (exit_text.get_height() / 2)))
    if goal == -1:
        pygame.draw.rect(screen, BUTTON_FONT_COLOR_green, level_button_1)
        pygame.draw.rect(screen, BUTTON_FONT_COLOR_blue, level_button_2)
        pygame.draw.rect(screen, BUTTON_FONT_COLOR_red, level_button_3)
        screen.blit(level_text_1, (level_button_1.x + (level_button_1.width / 2) - (level_text_1.get_width() / 2),
                                level_button_1.y + (level_button_1.height / 2) - (level_text_1.get_height() / 2)))
        screen.blit(level_text_2, (level_button_2.x + (level_button_2.width / 2) - (level_text_2.get_width() / 2),
                                level_button_2.y + (level_button_2.height / 2) - (level_text_2.get_height() / 2)))
        screen.blit(level_text_3, (level_button_3.x + (level_button_3.width / 2) - (level_text_3.get_width() / 2),
                                level_button_3.y + (level_button_3.height / 2) - (level_text_3.get_height() / 2)))
    if goal != mistake and goal != -1 and ball != 10:
        pygame.draw.rect(screen, BUTTON_COLOR, flip_button)
        screen.blit(flip_text, (flip_button.x + (flip_button.width / 2) - (flip_text.get_width() / 2),
                                flip_button.y + (flip_button.height / 2) - (flip_text.get_height() / 2)))

# Function to draw the flip result
def draw_flip_result():
    result_text = FONT.render(flip_result, True, FONT_COLOR)
    screen.blit(result_text, (MARGIN, MARGIN + BUTTON_SIZE[1] + MARGIN))

# Function to draw the flip count
def draw_flip_count():
    total_flips = heads + tails
    if total_flips > 0:
        heads_percentage = (heads / total_flips) * 100
        tails_percentage = (tails / total_flips) * 100
    else:
        heads_percentage = 0
        tails_percentage = 0

    heads_text = FONT.render(f"Heads: {heads} ({heads_percentage:.2f}%)", True, FONT_COLOR)
    tails_text = FONT.render(f"Tails: {tails} ({tails_percentage:.2f}%)", True, FONT_COLOR)
    screen.blit(heads_text, (MARGIN, MARGIN + BUTTON_SIZE[1] + MARGIN * 2))
    screen.blit(tails_text, (MARGIN, MARGIN + BUTTON_SIZE[1] + MARGIN * 3))

# Function to render text on screen
def render_text(text, font, surface, pos, color):
    text_surface = font.render(str(text), True, color)
    surface.blit(text_surface, pos)

# Function to handle events
def handle_events():
    global flip_result, flips, heads, tails, current_frame, animation_finished, text_surface, text, ball, mistake, goal
    if text_surface:
        screen.blit(text_surface, (160, 170))
    text_surface = FONT.render(text, True, FONT_COLOR)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN:
            mouse_pos = pygame.mouse.get_pos()
            if flip_button.collidepoint(mouse_pos):
                flips += 1
                result = random.choice(["heads", "tails"])
                if result == "heads":
                    heads += 1
                else:
                    tails += 1
                if text == result:
                    ball += 1
                else:
                    mistake += 1
                flip_result = result
                current_frame = 0
                animation_finished = False  # Reset animation status
                flip_sound.play()  # Play the flip sound
            if exit_button.collidepoint(mouse_pos):
                pygame.mixer.music.stop()
                pygame.quit()
                exit()
            if level_button_1.collidepoint(mouse_pos):
                goal = 20
            if level_button_2.collidepoint(mouse_pos):
                goal = 10
            if level_button_3.collidepoint(mouse_pos):
                goal = 5

        # Check for key presses
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_BACKSPACE:
                # If the user pressed backspace, remove the last character
                text = text[:-1]
            else:
                # Otherwise, add the character to the text
                text += event.unicode
                typing = True

# Load background image
background_image = pygame.image.load("Logo_astana_it_university.png")

# Game loop
running = True
flip_sound_4.set_volume(0.2)
flip_sound_4.play()
last_frame_time = pygame.time.get_ticks()  # Store the time of the last frame
while running:
    screen.fill(BACKGROUND_COLOR)
    screen.blit(background_image, (0, 0))
    draw_buttons()
    draw_flip_result()
    draw_flip_count()
    ball_1 = "You guessed:"
    ball_2 = "Try to guess:"
    ball_3 = "YOU WIN"
    ball_4 = "YOU LOSE"
    ball_5 = "Mistakes:"
    ball_6 = "You will lose if take the limit:"
    render_text(ball_2, FONT, screen, (20, 170), (0, 0, 0))
    render_text(ball_1, FONT, screen, (20, 150), (0, 0, 0))
    render_text(ball_5, FONT, screen, (20, 190), (0, 0, 0))
    render_text(str(mistake), FONT, screen, (120, 190), (0, 0, 0))
    render_text(ball_6, FONT, screen, (20, 210), (0, 0, 0))
    if goal != -1:
        render_text(str(goal), FONT, screen, (325, 210), (0, 0, 0))
    else:
        render_text("You must choose the level!!!!", FONT, screen, (325, 210), (255, 0, 0))
    render_text(ball, FONT, screen, (170,150), (0, 0, 0))
    if ball == 10:
        render_text(ball_3, FONT, screen, (500, 100), (0, 255, 0))
    if goal == mistake:
        render_text(ball_4, FONT, screen, (500, 100), (255, 0, 0))
    handle_events()
    if flip_result:
        draw_animation()
    current_time = pygame.time.get_ticks()  # Get the current time
    elapsed_time = current_time - last_frame_time  # Calculate the time since the last frame
    if elapsed_time < ANIMATION_DELAY:
        pygame.time.wait(ANIMATION_DELAY - elapsed_time)
    last_frame_time = pygame.time.get_ticks()  # Update the last frame time
    pygame.display.flip()
