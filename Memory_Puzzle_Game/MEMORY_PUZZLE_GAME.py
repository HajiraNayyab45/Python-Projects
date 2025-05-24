import pygame
import random
import time
from pygame.locals import *

# Initialize pygame
pygame.init()

# Constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
GRID_SIZE = 4  # 4x4 grid
CARD_SIZE = 100
GAP_SIZE = 10
FPS = 30
TIME_LIMIT = 60  # seconds

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (200, 200, 200)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)

# Calculate grid starting position for center alignment
GRID_WIDTH = GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1) * GAP_SIZE
GRID_HEIGHT = GRID_SIZE * CARD_SIZE + (GRID_SIZE - 1) * GAP_SIZE
GRID_START_X = (WINDOW_WIDTH - GRID_WIDTH) // 2
GRID_START_Y = (WINDOW_HEIGHT - GRID_HEIGHT) // 2 + 50  # Add space for the header

# Setup screen
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Memory Puzzle Game")
font = pygame.font.Font(None, 72)
small_font = pygame.font.Font(None, 36)
clock = pygame.time.Clock()

# Create the board
def create_board():
    symbols = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H'] * 2  # Duplicate symbols for pairs
    random.shuffle(symbols)
    board = []
    for row in range(GRID_SIZE):
        board.append(symbols[row * GRID_SIZE:(row + 1) * GRID_SIZE])
    return board

# Draw the board with center alignment
def draw_board(board, revealed, remaining_time):
    screen.fill(WHITE)

    # Draw header background
    pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 80))  # Header background

    # Draw header text
    header_text = font.render("Memory Puzzle Game", True, BLACK)
    header_rect = header_text.get_rect(center=(WINDOW_WIDTH // 2, 40))  # Centered in the header
    screen.blit(header_text, header_rect)

    # Draw timer below the header
    timer_text = small_font.render(f"Time: {remaining_time}s", True, BLACK)
    timer_rect = timer_text.get_rect(center=(WINDOW_WIDTH // 2, 100))  # Below the header
    screen.blit(timer_text, timer_rect)

    # Draw grid
    for row in range(GRID_SIZE):
        for col in range(GRID_SIZE):
            x = GRID_START_X + col * (CARD_SIZE + GAP_SIZE)
            y = GRID_START_Y + row * (CARD_SIZE + GAP_SIZE)
            if revealed[row][col]:
                pygame.draw.rect(screen, GRAY, (x, y, CARD_SIZE, CARD_SIZE))
                text = font.render(board[row][col], True, BLACK)
                text_rect = text.get_rect(center=(x + CARD_SIZE // 2, y + CARD_SIZE // 2))
                screen.blit(text, text_rect)
            else:
                pygame.draw.rect(screen, BLUE, (x, y, CARD_SIZE, CARD_SIZE))

# Draw buttons
def draw_buttons():
    play_again_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 - 50, 200, 50)
    exit_button = pygame.Rect(WINDOW_WIDTH // 2 - 100, WINDOW_HEIGHT // 2 + 20, 200, 50)

    # Change button colors here
    pygame.draw.rect(screen, (0, 128, 255), play_again_button)  # Blue color for "Play Again"
    pygame.draw.rect(screen, (255, 165, 0), exit_button)        # Orange color for "Exit"

    play_again_text = small_font.render("Play Again", True, BLACK)
    exit_text = small_font.render("Exit", True, BLACK)

    screen.blit(play_again_text, (play_again_button.x + 50, play_again_button.y + 10))
    screen.blit(exit_text, (exit_button.x + 75, exit_button.y + 10))

    return play_again_button, exit_button
# End screen
def display_end_message(message, background_color):
    screen.fill(background_color)  # Set background color (red for lose, green for win)
    pygame.draw.rect(screen, GRAY, (0, 0, WINDOW_WIDTH, 80))  # Header background
    header_text = font.render("Memory Puzzle Game", True, BLACK)
    header_rect = header_text.get_rect(center=(WINDOW_WIDTH // 2, 40))
    screen.blit(header_text, header_rect)

    # Display the end message
    end_text = font.render(message, True, WHITE)
    end_rect = end_text.get_rect(center=(WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2 - 150))
    screen.blit(end_text, end_rect)

    # Draw buttons
    play_again_button, exit_button = draw_buttons()
    pygame.display.flip()

    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = event.pos
                if play_again_button.collidepoint(mouse_x, mouse_y):
                    return True  # Restart the game
                elif exit_button.collidepoint(mouse_x, mouse_y):
                    pygame.quit()
                    exit()

# Main game function
def main():
    while True:  # Allow restarting the game
        board = create_board()
        revealed = [[False] * GRID_SIZE for _ in range(GRID_SIZE)]
        first_card = None
        start_time = time.time()

        running = True
        while running:
            elapsed_time = time.time() - start_time
            remaining_time = max(0, TIME_LIMIT - int(elapsed_time))

            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    exit()
                elif event.type == MOUSEBUTTONDOWN and event.button == 1:
                    mouse_x, mouse_y = event.pos
                    col = (mouse_x - GRID_START_X) // (CARD_SIZE + GAP_SIZE)
                    row = (mouse_y - GRID_START_Y) // (CARD_SIZE + GAP_SIZE)
                    if 0 <= row < GRID_SIZE and 0 <= col < GRID_SIZE and not revealed[row][col]:
                        revealed[row][col] = True
                        if first_card is None:
                            first_card = (row, col)
                        else:
                            r1, c1 = first_card
                            r2, c2 = row, col
                            if board[r1][c1] != board[r2][c2]:
                                pygame.time.wait(500)
                                revealed[r1][c1] = False
                                revealed[r2][c2] = False
                            first_card = None

            # Check win condition
            if all(all(row) for row in revealed):
                if display_end_message("🏆Congratulations You Win!", GREEN):
                    break  # Restart the game
                else:
                    return

            # Check time limit
            if remaining_time == 0:
                if display_end_message("😔Oh no, Time's Up!", RED):
                    break  # Restart the game
                else:
                    return

            # Draw everything
            draw_board(board, revealed, remaining_time)
            pygame.display.flip()
            clock.tick(FPS)

if __name__ == "__main__":
    main()