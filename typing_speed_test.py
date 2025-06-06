import pygame
import sys
import time

# Initialize pygame
pygame.init()

# Window settings
WIDTH, HEIGHT = 800, 600
win = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Typing Speed Test")

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
MAGENTA = (255, 0, 255)
CYAN = (0, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
GRAY = (100, 100, 100)

# Fonts
FONT = pygame.font.Font(None, 32)
BIG_FONT = pygame.font.Font(None, 48)

# Sounds
pygame.mixer.init()
try:
    type_sound = pygame.mixer.Sound('sounds/typeSec.mp3')
    success_sound = pygame.mixer.Sound('sounds/successMessage.mp3')
except pygame.error as e:
    print("Sound error:", e)
    type_sound = None
    success_sound = None

# Typing test sentence
TEXT = ("The quick brown fox jumps over the lazy dog, is a sentence containing "
        "all the letters of the alphabet.")

def draw_text_per_char(surface, text, typed_text, pos, font, max_width):
    x, y = pos
    space = font.size(' ')[0]
    for i, char in enumerate(text):
        char_width = font.size(char)[0] if char != ' ' else space

        if x + char_width > max_width:
            x = pos[0]
            y += font.get_height() + 5

        if i < len(typed_text):
            color = MAGENTA if typed_text[i] == char else CYAN
        else:
            color = WHITE

        char_surface = font.render(char, True, color)
        surface.blit(char_surface, (x, y))
        x += char_width

def button(surface, text, rect, color_idle, color_hover, action=None):
    mouse = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()

    if rect.collidepoint(mouse):
        pygame.draw.rect(surface, color_hover, rect)
        if click[0] == 1 and action:
            action()
    else:
        pygame.draw.rect(surface, color_idle, rect)

    text_surface = FONT.render(text, True, WHITE)
    text_rect = text_surface.get_rect(center=rect.center)
    surface.blit(text_surface, text_rect)

def draw_center_text(text, pos, font, color):
    text_surface = font.render(text, True, color)
    text_rect = text_surface.get_rect(center=pos)
    win.blit(text_surface, text_rect)

def start_screen():
    waiting = True

    def stop_waiting():
        nonlocal waiting
        waiting = False

    while waiting:
        win.fill(BLACK)
        draw_center_text("Welcome to Typing Speed Test!", (WIDTH // 2, 100), BIG_FONT, GREEN)
        draw_center_text("Click START to begin typing.", (WIDTH // 2, 200), FONT, WHITE)

        btn_rect = pygame.Rect(WIDTH // 2 - 100, HEIGHT // 2, 200, 50)
        button(win, "START", btn_rect, GRAY, CYAN, action=stop_waiting)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(60)

def show_final_score(wpm, cpm, elapsed_time):
    waiting = True

    def restart():
        nonlocal waiting
        waiting = False
        typing_test()

    def quit_game():
        pygame.quit()
        sys.exit()

    while waiting:
        win.fill(BLACK)

        draw_center_text("Test Complete!", (WIDTH // 2, 100), BIG_FONT, GREEN)
        draw_center_text(f"Final WPM: {wpm}", (WIDTH // 2, 200), FONT, WHITE)
        draw_center_text(f"Final CPM: {cpm}", (WIDTH // 2, 250), FONT, WHITE)
        draw_center_text(f"Total Time: {round(elapsed_time, 2)} seconds", (WIDTH // 2, 300), FONT, WHITE)

        restart_btn_rect = pygame.Rect(WIDTH // 2 - 150, HEIGHT // 2 + 100, 120, 50)
        quit_btn_rect = pygame.Rect(WIDTH // 2 + 30, HEIGHT // 2 + 100, 120, 50)

        button(win, "RESTART", restart_btn_rect, GRAY, CYAN, action=restart)
        button(win, "QUIT", quit_btn_rect, GRAY, RED, action=quit_game)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

        pygame.time.Clock().tick(60)

def typing_test():
    clock = pygame.time.Clock()
    running = True
    typed_text = ""
    start_time = None
    finished = False
    submitted = False
    elapsed_time = 0
    wpm = 0
    cpm = 0

    def submit():
        nonlocal submitted
        submitted = True
        for _ in range(3):
            for color in [CYAN, RED, MAGENTA]:
                win.fill(color)
                pygame.display.update()
                pygame.time.delay(300)
        show_final_score(wpm, cpm, elapsed_time)

    while running:
        win.fill(BLACK)

        draw_text_per_char(win, TEXT, typed_text, (50, 50), FONT, WIDTH - 50)

        if start_time:
            elapsed_time = max(time.time() - start_time, 1)
            cpm = int(len(typed_text) / (elapsed_time / 60))
            wpm = round(cpm / 5, 2)

            draw_center_text(f"WPM: {wpm}", (WIDTH // 2, 450), FONT, GREEN)
            draw_center_text(f"CPM: {cpm}", (WIDTH // 2, 500), FONT, GREEN)
            draw_center_text(f"Time: {round(elapsed_time, 2)} s", (WIDTH // 2, 550), FONT, GREEN)

        if finished and not submitted:
            submit_btn_rect = pygame.Rect(WIDTH // 2 - 75, HEIGHT - 100, 150, 50)
            button(win, "SUBMIT", submit_btn_rect, GRAY, GREEN, action=submit)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                sys.exit()

            if event.type == pygame.KEYDOWN and not finished:
                if start_time is None:
                    start_time = time.time()

                if event.key == pygame.K_ESCAPE:
                    running = False
                    sys.exit()
                elif event.key == pygame.K_BACKSPACE:
                    typed_text = typed_text[:-1]
                else:
                    char = event.unicode
                    if len(typed_text) < len(TEXT):
                        typed_text += char
                        if type_sound:
                            type_sound.play()

                if typed_text == TEXT:
                    finished = True
                    if success_sound:
                        success_sound.play()

        clock.tick(60)

# Run the game
start_screen()
typing_test()
pygame.quit()
sys.exit()
