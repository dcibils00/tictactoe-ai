"""
Tic Tac Toe, also known as "Noughts and Crosses," has origins dating back to ancient times. 
Early versions of the game were played in ancient Egypt around 1300 BCE and by the Romans in the 1st century BCE with a game called Terni Lapilli. 
These early forms involved marking grids or placing stones to create rows, though they often had different rules from the modern version.

The game we know today became popular in the 19th and 20th centuries as a simple pencil-and-paper pastime. 
With its straightforward rules, it spread quickly across schools and homes, becoming a favorite for children and adults alike. 
The goal was clear: alternate between X's and O's, trying to form a row of three horizontally, vertically, or diagonally.

In 1952, Tic Tac Toe made history as one of the first games to be programmed into a computer with a game called OXO. 
This marked an early step in artificial intelligence, as machines could calculate moves and compete against humans. 
Today, Tic Tac Toe remains a universal game, enjoyed for its simplicity and its value in teaching logic and strategy.

This version in Python was developed for fun only so I have tic tac toe on my mac. Enjoy.

Diego Cibils.
2024
"""
import pygame
import sys
import time
from pygame.locals import *

# Initialize Pygame
pygame.init()

# Screen dimensions and colors
SCREEN_WIDTH, SCREEN_HEIGHT = 600, 650
LINE_COLOR = (0, 0, 0)
BACKGROUND_COLOR = (255, 255, 255)
STATUS_BACKGROUND_COLOR = (200, 200, 200)
TEXT_COLOR = (0, 0, 0)
BUTTON_COLOR = (100, 100, 255)
BUTTON_TEXT_COLOR = (255, 255, 255)
CELL_SIZE = 200
CIRCLE_COLOR = (255, 255, 255)
CROSS_COLOR = (255, 153, 0)
LINE_WIDTH = 5

# SET DIFFICULTY for the AI ALGORITHM
# Max Depth = 9: Unbeatable AI that always wins or ties.
# Max Depth = 3–4: Fun and challenging AI that occasionally makes mistakes.
# Max Depth = 2: Easy AI for casual players.

MAX_DEPTH = 5  # Default: Medium AI

# Fonts
pygame.font.init()
font = pygame.font.SysFont('Arial', 50)
status_font = pygame.font.SysFont('Arial', 20)

# Load the background texture
background_texture = pygame.image.load("orange.jpg")
background_texture = pygame.transform.scale(background_texture, (SCREEN_WIDTH, SCREEN_HEIGHT - 50))

# Initialize screen
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tic Tac Toe - AI")

# Board
board = [[" " for _ in range(3)] for _ in range(3)]

# Current player (X for human, O for AI)
current_player = "X"

# Game state
game_over = False
move_count = 0  # Counts the number of moves made in the game
status_message = ""


def draw_board():
    """Draws the Tic Tac Toe grid and current board state."""
    # Draw the background texture
    screen.blit(background_texture, (0, 0))
    
    # Draw the grid lines
    for i in range(1, 3):
        pygame.draw.line(screen, LINE_COLOR, (0, CELL_SIZE * i), (SCREEN_WIDTH, CELL_SIZE * i), LINE_WIDTH)
        pygame.draw.line(screen, LINE_COLOR, (CELL_SIZE * i, 0), (CELL_SIZE * i, SCREEN_HEIGHT - 50), LINE_WIDTH)

    # Draw X's and O's
    for row in range(3):
        for col in range(3):
            cell_x = col * CELL_SIZE + CELL_SIZE // 2
            cell_y = row * CELL_SIZE + CELL_SIZE // 2
            if board[row][col] == "X":
                pygame.draw.line(screen, CROSS_COLOR, (cell_x - 50, cell_y - 50), (cell_x + 50, cell_y + 50), LINE_WIDTH)
                pygame.draw.line(screen, CROSS_COLOR, (cell_x + 50, cell_y - 50), (cell_x - 50, cell_y + 50), LINE_WIDTH)
            elif board[row][col] == "O":
                pygame.draw.circle(screen, CIRCLE_COLOR, (cell_x, cell_y), 50, LINE_WIDTH)


def draw_status():
    """Draws the status message and rematch button if game over."""
    pygame.draw.rect(screen, STATUS_BACKGROUND_COLOR, (0, SCREEN_HEIGHT - 50, SCREEN_WIDTH, 50))
    status_surface = status_font.render(status_message, True, TEXT_COLOR)
    screen.blit(status_surface, (20, SCREEN_HEIGHT - 40))

    if game_over:
        button_rect = pygame.Rect((SCREEN_WIDTH - 120, SCREEN_HEIGHT - 45), (100, 40))
        pygame.draw.rect(screen, BUTTON_COLOR, button_rect)
        button_text = status_font.render("Rematch", True, BUTTON_TEXT_COLOR)
        screen.blit(button_text, (SCREEN_WIDTH - 120 + 10, SCREEN_HEIGHT - 40))
        return button_rect
    return None


def check_winner():
    """Checks if there's a winner or if the game is a tie."""
    # Check rows for a winner
    for row in range(3):
        if board[row][0] == board[row][1] == board[row][2] and board[row][0] != " ":
            return board[row][0]

    # Check columns for a winner
    for col in range(3):
        if board[0][col] == board[1][col] == board[2][col] and board[0][col] != " ":
            return board[0][col]

    # Check diagonals for a winner
    if board[0][0] == board[1][1] == board[2][2] and board[0][0] != " ":
        return board[0][0]
    if board[0][2] == board[1][1] == board[2][0] and board[0][2] != " ":
        return board[0][2]

    # Check for a tie (all cells filled and no winner)
    if all(board[row][col] != " " for row in range(3) for col in range(3)):
        return "Tie"

    # Game is still ongoing
    return None


def get_ai_move():
    """Uses the Minimax algorithm to calculate the best move for the AI."""
    best_score = float('-inf')  # AI wants to maximize the score
    best_move = None

    for row in range(3):
        for col in range(3):
            if board[row][col] == " ":
                # Try this move
                board[row][col] = "O"
                score = minimax(board, 0, False)  # AI is maximizing
                board[row][col] = " "  # Undo the move

                # Choose the best move
                if score > best_score:
                    best_score = score
                    best_move = (row, col)

    return best_move


def minimax(board, depth, is_maximizing):
    """Recursive Minimax algorithm with a limited depth."""
    if depth == MAX_DEPTH:  # Stop recursion at a certain depth
        return 0  # Neutral score for partial evaluation

    result = check_winner()
    if result == "O":  # AI wins
        return 10 - depth
    elif result == "X":  # Player wins
        return depth - 10
    elif result == "Tie":  # Tie
        return 0

    if is_maximizing:
        best_score = float('-inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "O"
                    score = minimax(board, depth + 1, False)
                    board[row][col] = " "
                    best_score = max(score, best_score)
        return best_score
    else:
        best_score = float('inf')
        for row in range(3):
            for col in range(3):
                if board[row][col] == " ":
                    board[row][col] = "X"
                    score = minimax(board, depth + 1, True)
                    board[row][col] = " "
                    best_score = min(score, best_score)
        return best_score


def reset_game():
    """Resets the game state for a rematch."""
    global board, current_player, game_over, move_count, status_message
    board = [[" " for _ in range(3)] for _ in range(3)]
    current_player = "X"
    game_over = False
    move_count = 0
    status_message = ""


def main():
    global current_player, game_over, move_count, status_message

    while True:
        draw_board()
        rematch_button = draw_status()

        if game_over:
            status_message = f"{winner} Wins!" if winner != "Tie" else "It's a Tie!"

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                sys.exit()

            if game_over and event.type == MOUSEBUTTONDOWN:
                mouse_x, mouse_y = event.pos
                if rematch_button and rematch_button.collidepoint(mouse_x, mouse_y):
                    reset_game()

            if event.type == MOUSEBUTTONDOWN and not game_over and current_player == "X":
                mouse_x, mouse_y = event.pos
                if mouse_y < SCREEN_HEIGHT - 50:
                    row, col = mouse_y // CELL_SIZE, mouse_x // CELL_SIZE
                    if board[row][col] == " ":
                        board[row][col] = "X"
                        move_count += 1

                         # Delay AI move to simulate thinking
                        pygame.display.update()
                        time.sleep(0.4)

                        # Check for a winner or tie
                        winner = check_winner()
                        if winner:
                            game_over = True
                            continue

                        current_player = "O"

                        if not game_over:
                            move = get_ai_move()
                            if move:
                                board[move[0]][move[1]] = "O"
                                move_count += 1

                                # Check for a winner or tie
                                winner = check_winner()
                                if winner:
                                    game_over = True
                                    continue

                                current_player = "X"

        pygame.display.flip()


if __name__ == "__main__":
    main()
