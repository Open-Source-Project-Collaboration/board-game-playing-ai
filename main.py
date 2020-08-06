import pygame


class GameState:
    def __init__(self):
        self.board = [["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
                      ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["--", "--", "--", "--", "--", "--", "--", "--"],
                      ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
                      ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"]]


def load_images():
    for item in game_state.board:
        for piece in item:
            if piece != "--":
                pieces_images[piece] = pygame.transform.scale(pygame.image.load("Images/" + piece + ".png"),
                                                              (square_size, square_size))


def draw_board():
    for r in range(squares):
        for c in range(squares):
            color = colors[(r + c) % 2]  # Picks either the white square or the black one
            screen.blit(color, pygame.Rect(r * square_size, c * square_size, square_size, square_size))  # Adds the
            # picked square


def draw_pieces(gs):
    for r in range(squares):
        for c in range(squares):
            piece = gs.board[r][c]  # Gets the piece on the square in GameState.board
            if piece != "--":  # If the square is not empty
                screen.blit(pieces_images[piece],
                            pygame.Rect(c * square_size, r * square_size, square_size, square_size))


if __name__ == "__main__":
    pygame.init()
    width = height = 512  # Game will run at 512 x 512
    screen = pygame.display.set_mode((width, height))
    colors = [pygame.image.load("Images/White.png"), pygame.image.load("Images/Black.png")]  # The black square and the
    # white square images
    squares = 8
    square_size = height // squares
    game_state = GameState()
    pieces_images = {}  # A dictionary with the chess piece notations as keys and the images as values
    load_images()
    draw_board()
    draw_pieces(game_state)
    while True:
        for event in pygame.event.get():  # Checks if the game is still running
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()  # updates the screen
        draw_pieces(game_state)
