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

        self.white_turn = True

    def make_move(self, start_row, start_column, end_row, end_column):
        piece = self.board[start_row][start_column]
        if self.white_turn and piece[0] == 'w' or not self.white_turn and piece[0] == 'b':
            if piece != "--":
                self.board[start_row][start_column] = '--'
                self.board[end_row][end_column] = piece
                self.white_turn = not self.white_turn


def load_images():  # Loads the images of the pieces
    for item in game_state.board:
        for piece in item:
            if piece != "--":
                pieces_images[piece] = pygame.transform.scale(pygame.image.load("Images/" + piece + ".png"),
                                                              (square_size, square_size))


def draw_board():
    for r in range(squares):
        for c in range(squares):
            color = colors[(r + c) % 2]  # Picks either the white square or the black one
            screen.blit(color, pygame.Rect(c * square_size, r * square_size, square_size, square_size))  # Adds the
            # picked square
            if (r, c) in highlighted_squares:
                screen.blit(colors[2], pygame.Rect(c * square_size, r * square_size, square_size, square_size))


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
    pygame.display.set_caption("Chess")
    colors = [pygame.image.load("Images/White.png"), pygame.image.load("Images/Black.png"),
              pygame.image.load("Images/Highlight.png")]
    # The black square, white square images and highlight square images
    squares = 8
    square_size = height // squares
    game_state = GameState()
    pieces_images = {}  # A dictionary with the chess piece notations as keys and the images as values
    load_images()
    moves = []  # Moves list will have a maximum length of two values as tuples containing the start square and the end
    # square
    valid_moves = []  # A list of lists containing
    # valid moves in the form [[(start_row, start_col), (end_row, end_col)], [...], [...]]
    highlighted_squares = []
    while True:
        move_made = False
        for event in pygame.event.get():  # Checks if the game is still running
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                column = pygame.mouse.get_pos()[0] // square_size
                row = pygame.mouse.get_pos()[1] // square_size
                selected_square = (row, column)
                moves.append(selected_square)
                highlighted_squares.append(selected_square)
                if (selected_square == moves[0] and len(moves) == 2) \
                        or (game_state.board[row][column] == "--" and len(moves) == 1):  # If the user selected the same
                    # piece in the second move or selected an empty square in the first move
                    moves = []  # Reset the moves list
                    highlighted_squares = []
                elif len(moves) == 2 and [moves[0], moves[1]] in valid_moves:
                    game_state.make_move(moves[0][0], moves[0][1], moves[1][0], moves[1][1])
                    moves = []
                    highlighted_squares = []
                    move_made = True
                elif len(moves) == 2 and [moves[0], moves[1]] not in valid_moves:
                    moves = []
                    highlighted_squares = []

        pygame.display.flip()  # updates the screen
        draw_board()
        draw_pieces(game_state)
