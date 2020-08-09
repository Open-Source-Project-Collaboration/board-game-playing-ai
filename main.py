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
        self.pawn_promotion = ()  # The row and column of the pawn to be promoted

    def make_move(self, start_row, start_column, end_row, end_column):
        piece = self.board[start_row][start_column]
        self.board[start_row][start_column] = '--'
        self.board[end_row][end_column] = piece
        self.white_turn = not self.white_turn

    def promote_pawn(self, r, c, piece):
        self.board[r][c] = piece

    def get_pawn_moves(self, r, c):  # TODO: Add "en passant"
        valid_moves_return = []

        if self.board[r][c][0] == 'w':
            next_row = r - 1
            next_two_rows = r - 2
            opponent_piece = 'b'
        else:
            next_row = r + 1
            next_two_rows = r + 2
            opponent_piece = 'w'

        if next_row not in [-1, 8]:  # To avoid list index error when pawn is at the edge
            if self.board[next_row][c] == '--':  # Empty square in front of pawn
                valid_moves_return.append([(r, c), (next_row, c)])
                if (r == 6 or r == 1) and self.board[next_two_rows][c] == '--':  # Two empty squares in front of pawn
                    # before moving it
                    valid_moves_return.append([(r, c), (next_two_rows, c)])
            if c != 0 and self.board[next_row][c - 1][0] == opponent_piece:  # Opponent piece placed diagonally adjacent
                valid_moves_return.append([(r, c), (next_row, c - 1)])
            if c != 7 and self.board[next_row][c + 1][0] == opponent_piece:  # Same but the other side of the diagonal
                valid_moves_return.append([(r, c), (next_row, c + 1)])

            return valid_moves_return
        else:
            self.pawn_promotion = (r, c)


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

    if game_state.pawn_promotion != ():  # If there is a pawn to be promoted
        surface = pygame.Surface((width, height))
        surface.set_alpha(100)
        surface.fill((0, 0, 0))
        screen.blit(surface, (0, 0))  # The semi transparent black square overlay
        pawn_row = game_state.pawn_promotion[0]
        pawn_column = game_state.pawn_promotion[1]
        pawn_color = game_state.board[pawn_row][pawn_column][0]
        for i in range(0, 4):
            piece_to_show = pawn_color + promotions[i]
            # The co-ordinates for arranging the piece promotion choices in the middle
            piece_at_x = ((squares // 2) + i - 2) * square_size
            piece_at_y = (squares // 2) * square_size
            screen.blit(pieces_images[piece_to_show], pygame.Rect(piece_at_x, piece_at_y, square_size, square_size))
        screen.blit(promotion_text,
                    pygame.Rect(width // 2 - round(square_size * 3.5), square_size, square_size * 4, square_size * 4))


def draw_pieces(gs):
    for r in range(squares):
        for c in range(squares):
            piece = gs.board[r][c]  # Gets the piece on the square in GameState.board
            if piece != "--":  # If the square is not empty
                screen.blit(pieces_images[piece],
                            pygame.Rect(c * square_size, r * square_size, square_size, square_size))


def get_valid_moves():
    for r in range(squares):
        for c in range(squares):
            if game_state.board[r][c][1] == "P":
                available_moves = game_state.get_pawn_moves(r, c)
                if available_moves is not None:
                    for item in available_moves:
                        valid_moves.append(item)


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
    promotions = ['B', 'N', 'R', 'Q']  # The pieces available for pawn promotion
    font = pygame.font.SysFont("Arial", 24)  # The font which the game will use
    promotion_text = font.render("To which piece would you like to promote the pawn?", True, (255, 255, 255))
    load_images()
    moves = []  # Moves list will have a maximum length of two values as tuples containing the start square and the end
    # square

    valid_moves = []  # A list of lists containing
    # valid moves in the form [[(start_row, start_col), (end_row, end_col)], [...], [...]]

    highlighted_squares = []
    get_valid_moves()
    while True:
        move_made = False
        for event in pygame.event.get():  # Checks if the game is still running

            if event.type == pygame.QUIT:
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                column = pygame.mouse.get_pos()[0] // square_size
                row = pygame.mouse.get_pos()[1] // square_size
                selected_square = (row, column)
                piece_selected = game_state.board[row][column]

                if game_state.pawn_promotion != ():
                    piece_promote_index = column + 2 - squares // 2  # The list index of the piece to which the pawn is
                    # promoted
                    piece_row = game_state.pawn_promotion[0]  # The row of the pawn to be promoted
                    piece_column = game_state.pawn_promotion[1]  # The column of the pawn to be promoted
                    piece_color = game_state.board[piece_row][piece_column][0]  # The color of the pawn to be promoted
                    piece_promote = piece_color + promotions[piece_promote_index]
                    # The piece to which the pawn is promoted ie: 'wQ'

                    game_state.promote_pawn(piece_row, piece_column, piece_promote)
                    game_state.pawn_promotion = ()

                elif len(moves) == 0 and (game_state.white_turn and piece_selected[0] != 'b'
                                          or not game_state.white_turn and piece_selected[0] != 'w') or len(moves) >= 1:
                    # If it is white's turn and the piece selected is not black or it is black's turn and the piece
                    # selected is not white ie: "-" or "b", that is on the first click only. This is ignored on the
                    # second click

                    moves.append(selected_square)
                    highlighted_squares.append(selected_square)

                    for valid_move in valid_moves:
                        if len(moves) == 1 and valid_move[0] == selected_square:  # Adds the valid moves of the selected
                            # piece to the highlighted squares
                            highlighted_squares.append(valid_move[1])

                    if (selected_square == moves[0] and len(moves) == 2) \
                            or (piece_selected == "--" and len(moves) == 1):
                        # If the user selected the same piece in the second move or selected an empty square in the
                        # first move
                        moves = []  # Reset the moves list
                        highlighted_squares = []

                    elif len(moves) == 2 and [moves[0], moves[1]] in valid_moves:  # If the user picked a valid square
                        # at the second click
                        game_state.make_move(moves[0][0], moves[0][1], moves[1][0], moves[1][1])
                        moves = []
                        highlighted_squares = []
                        move_made = True
                        valid_moves = []

                    elif len(moves) == 2 and [moves[0], moves[1]] not in valid_moves:  # If the user didn't pick a valid
                        # square at the second click
                        moves = []
                        highlighted_squares = []

        pygame.display.flip()  # updates the screen
        if move_made:
            get_valid_moves()
            move_made = False
        draw_board()
        if game_state.pawn_promotion == ():
            draw_pieces(game_state)
