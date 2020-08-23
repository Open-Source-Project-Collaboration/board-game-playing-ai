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
        self.en_passant = []  # The row and the column of the pawn that can perform an 'en passant'
        self.en_passant_length = -1  # The required length of the move log in order to do 'en passant'
        # This variable is used to cancel the en passant ability if other moves were made

        self.move_log = []  # A list containing all moves performed
        self.castling = [(0, 7), (7, 0), (0, 0), (7, 7)]

    def make_move(self, move):
        piece = self.board[move.start_row][move.start_column]
        self.board[move.start_row][move.start_column] = '--'  # Replace the starting square with an empty one
        self.board[move.end_row][move.end_column] = piece  # Replace the ending square with the piece

        if self.en_passant:
            if self.en_passant_length != len(self.move_log):
                self.en_passant = []
            if (move.start_row, move.start_column) in self.en_passant:
                # If the current piece (pawn) has an ability to do en passant

                if move.piece_to_move[0] == 'w':
                    move.piece_to_capture = self.board[move.end_row + 1][move.end_column]
                    self.board[move.end_row + 1][move.end_column] = "--"
                    move.end_row, move.end_column = move.end_row + 1, move.end_column
                    # To avoid bugs when undoing en passant moves

                    self.en_passant = []

                elif move.piece_to_move[0] == "b":
                    move.piece_to_capture = self.board[move.end_row - 1][move.end_column]
                    self.board[move.end_row - 1][move.end_column] = "--"
                    move.end_row, move.end_column = move.end_row - 1, move.end_column
                    # To avoid bugs when undoing en passant moves

                    self.en_passant = []

        if move.piece_to_move[1] == "K":
            kingside_direction = 1  # The left side of the king
            if abs(move.end_column - move.start_column) == 2:
                direction = (move.end_column - move.start_column) // 2  # Direction can be +1 or -1
                rook_to_castle_col = 7 if direction == kingside_direction else 0
                rook_to_castle = self.board[move.start_row][rook_to_castle_col]
                self.board[move.start_row][rook_to_castle_col] = '--'
                self.board[move.start_row][move.start_column + 1 * direction] = rook_to_castle
                # The rook jumps to the square over which the king crossed

            # Remove the possible castling moves in that row when the king is moved
            if (move.start_row, 0) in self.castling:
                self.castling.remove((move.start_row, 0))
            if (move.start_row, 7) in self.castling:
                self.castling.remove((move.start_row, 7))

        # If a rook is moved, remove its castling moves
        elif move.piece_to_move[1] == "R":
            if (move.start_row, move.start_column) in self.castling:
                self.castling.remove((move.start_row, move.start_column))

        self.white_turn = not self.white_turn
        self.move_log.append(move)

    def undo_move(self):  # Causes bugs with en passant and castling if used with them (no need to fix that since the
        # user won't be able to use the function)

        if self.move_log:  # If the move log is not empty
            move_to_undo = self.move_log.pop()  # The last move
            self.make_move(Move(move_to_undo.end_square, move_to_undo.start_square))
            # Makes the move in the opposite direction

            game_state.board[move_to_undo.end_row][move_to_undo.end_column] = move_to_undo.piece_to_capture
            # Returns the captured piece to its place

            del (self.move_log[-1])
            # Deletes the move in the opposite direction from the move log

    def promote_pawn(self, r, c, piece):
        self.board[r][c] = piece

    def get_pawn_moves(self, r, c):
        valid_moves_return = []
        pawn_color = self.board[r][c][0]

        if pawn_color == 'w':
            next_row = r - 1
            next_two_rows = r - 2
            opponent_piece_color = 'b'
            fifth_rank = 3  # The row at which the white pawn is at fifth rank
        else:
            next_row = r + 1
            next_two_rows = r + 2
            opponent_piece_color = 'w'
            fifth_rank = 4  # The row at which the black pawn is at fifth rank

        if next_row not in [-1, 8]:  # To avoid list index error when pawn is at the edge

            if self.board[next_row][c] == '--':  # Empty square in front of pawn
                valid_moves_return.append(Move((r, c), (next_row, c)))
                if (r == 6 and pawn_color == 'w') or (r == 1 and pawn_color == 'b') \
                        and self.board[next_two_rows][c] == '--':  # Two empty squares in front of pawn
                    # before moving it
                    valid_moves_return.append(Move((r, c), (next_two_rows, c)))

            if c != 0 and self.board[next_row][c - 1][0] == opponent_piece_color:
                # Opponent piece placed diagonally adjacent
                valid_moves_return.append(Move((r, c), (next_row, c - 1)))

            if c != 7 and self.board[next_row][c + 1][0] == opponent_piece_color:
                # Same but the other side of the diagonal
                valid_moves_return.append(Move((r, c), (next_row, c + 1)))

            # En Passant conditions
            if self.move_log:  # If there are moves in the move log
                last_move = self.move_log[-1]  # Sees the last move made
                if c != 0 and r == fifth_rank and self.board[r][c - 1][0] == opponent_piece_color and \
                        last_move.piece_to_move[1] == "P" and abs(last_move.end_row - last_move.start_row) == 2 \
                        and last_move.end_column == c - 1:
                    self.en_passant.append((r, c))
                    self.en_passant_length = len(self.move_log)
                    valid_moves_return.append(Move((r, c), (next_row, c - 1)))

                if c != 7 and r == fifth_rank and self.board[r][c + 1][0] == opponent_piece_color and \
                        last_move.piece_to_move[1] == "P" and abs(last_move.end_row - last_move.start_row) == 2 \
                        and last_move.end_column == c + 1:
                    self.en_passant.append((r, c))
                    self.en_passant_length = len(self.move_log)
                    valid_moves_return.append(Move((r, c), (next_row, c + 1)))

            return valid_moves_return
        else:
            self.pawn_promotion = (r, c)

    def get_knight_moves(self, r, c):
        valid_moves_return = []
        knight_color = self.board[r][c][0]
        next_two_rows = r - 2
        next_row = r - 1
        previous_two_rows = r + 2
        previous_row = r + 1

        for item in [next_row, previous_row]:  # One square horizontally, two squares vertically move
            if 0 <= item <= 7:
                if c + 2 <= 7 and self.board[item][c + 2][0] != knight_color:
                    valid_moves_return.append(Move((r, c), (item, c + 2)))
                if c - 2 >= 0 and self.board[item][c - 2][0] != knight_color:
                    valid_moves_return.append(Move((r, c), (item, c - 2)))

        for item in [next_two_rows, previous_two_rows]:  # Two squares horizontally, one square vertically move
            if 0 <= item <= 7:
                if c + 1 <= 7 and self.board[item][c + 1][0] != knight_color:
                    valid_moves_return.append(Move((r, c), (item, c + 1)))
                if c - 1 >= 0 and self.board[item][c - 1][0] != knight_color:
                    valid_moves_return.append(Move((r, c), (item, c - 1)))

        return valid_moves_return

    def get_queen_moves(self, r, c):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1), (0, 1), (1, 0), (-1, 0), (0, -1)]

        current_player = self.board[r][c][0]
        enemy_player = 'w' if current_player == 'b' else 'b'
        valid_moves_return = []
        for x, y in directions:
            for dist in range(1, 8):
                new_r, new_c = r + x * dist, c + y * dist
                if not 0 <= new_r <= 7 or not 0 <= new_c <= 7:
                    break
                current_tile = self.board[new_r][new_c][0]
                if current_tile == current_player:
                    break  # stop searching if we reach a friendly piece
                valid_moves_return.append(Move((r, c), (new_r, new_c)))  # for any other cases, it's a valid move
                if current_tile == enemy_player:
                    break  # stop searching if we reach an enemy piece
        return valid_moves_return

    def get_bishop_moves(self, r, c):
        directions = [(1, 1), (1, -1), (-1, 1), (-1, -1)]

        current_player = self.board[r][c][0]
        enemy_player = 'w' if current_player == 'b' else 'b'
        valid_moves_return = []
        for x, y in directions:
            for dist in range(1, 8):
                new_r, new_c = r + x * dist, c + y * dist
                if not 0 <= new_r <= 7 or not 0 <= new_c <= 7:
                    break
                current_tile = self.board[new_r][new_c][0]
                if current_tile == current_player:
                    break  # stop searching if we reach a friendly piece
                valid_moves_return.append(Move((r, c), (new_r, new_c)))  # for any other cases, it's a valid move
                if current_tile == enemy_player:
                    break  # stop searching if we reach an enemy piece
        return valid_moves_return

    def get_rook_moves(self, r, c):
        directions = [(0, 1), (1, 0), (-1, 0), (0, -1)]

        current_player = self.board[r][c][0]
        enemy_player = 'w' if current_player == 'b' else 'b'
        valid_moves_return = []
        for x, y in directions:
            for dist in range(1, 8):
                new_r, new_c = r + x * dist, c + y * dist
                if not 0 <= new_r <= 7 or not 0 <= new_c <= 7:
                    break
                current_tile = self.board[new_r][new_c][0]
                if current_tile == current_player:
                    break  # stop searching if we reach a friendly piece
                valid_moves_return.append(Move((r, c), (new_r, new_c)))  # for any other cases, it's a valid move
                if current_tile == enemy_player:
                    break  # stop searching if we reach an enemy piece
        if c in [0, 7]:
            castling_moves = game_state.get_castling(r, c)
            for item in castling_moves:
                available_moves.append(item)
        return valid_moves_return

    def get_castling(self, r, c):
        valid_moves_return = []
        directions = [1, -1]  # Directions that determine how the search will move
        for direction in directions:
            for dist in range(1, 5):
                if 0 <= c + dist * direction <= 7:
                    tile = self.board[r][c + dist * direction]
                    if tile != '--' and tile[1] != 'K':  # If it is neither an empty square nor a king
                        break
                    elif tile[1] == 'K' and (r, c) in self.castling:
                        # The king can jump two columns according to this formula
                        valid_moves_return.append(Move((r, c + dist * direction), (r, c + (dist - 2) * direction)))
                        break
        return valid_moves_return


class Move:  # A class to deal with moves performed
    def __init__(self, start_square, end_square):
        self.start_square = start_square
        self.end_square = end_square
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_to_move = game_state.board[self.start_row][self.start_column]
        self.piece_to_capture = game_state.board[self.end_row][self.end_column]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.move_id = self.start_row * 10000 + self.start_column * 100 + self.end_row * 10 + self.end_column

    def __eq__(self, other):
        if isinstance(other, Move):
            if self.move_id == other.move_id:
                return True
        return False


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
            pygame.draw.rect(screen, color, pygame.Rect(c * square_size, r * square_size, square_size, square_size))
            # Adds the picked square

            if (r, c) in highlighted_squares:
                screen.blit(colors[2], pygame.Rect(c * square_size, r * square_size, square_size, square_size))

    if game_state.pawn_promotion != ():  # If there is a pawn to be promoted
        surface = pygame.Surface((width, height))
        surface.set_alpha(100)
        surface.fill((0, 0, 0))
        screen.blit(surface, (0, 0))  # The semi-transparent black square overlay
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

    # Add a score / info tab at bottom of screen
    pygame.draw.rect(screen, (255, 255, 255), (0, 513, 512, 30))
    turn_text = status_font.render("White's Turn" if game_state.white_turn
                                   else "Black's Turn", True, (0, 0, 0), (255, 255, 255))
    screen.blit(turn_text, (5, 517))


def draw_pieces(gs):
    for r in range(squares):
        for c in range(squares):
            piece = gs.board[r][c]  # Gets the piece on the square in GameState.board
            if piece != "--":  # If the square is not empty
                screen.blit(pieces_images[piece],
                            pygame.Rect(c * square_size, r * square_size, square_size, square_size))


def get_valid_moves():
    available_moves = []

    for r in range(squares):
        for c in range(squares):
            piece = game_state.board[r][c][1]
            # Dictionary holding the pieces and their corresponding move function
            pieces_dict = {"P": game_state.get_pawn_moves, "N": game_state.get_knight_moves,
                           "B": game_state.get_bishop_moves, "R": game_state.get_rook_moves,
                           "Q": game_state.get_queen_moves}  # Add 'K' when get_king_moves function is made
            if piece in pieces_dict:
                available_moves = pieces_dict[piece](r, c)  # Reference the dict to find the pieces possible moves

            for item in available_moves:
                if item.piece_to_capture[1] != 'K':
                    valid_moves.append(item)


if __name__ == "__main__":
    pygame.init()
    width = height = 512  # Game will run at 512 x 512
    bar_height = 30
    screen = pygame.display.set_mode((width, height + bar_height))
    pygame.display.set_caption("Chess")
    squares = 8
    square_size = height // squares

    white_color = (250, 235, 239)
    black_color = (153, 164, 231)
    green_color = (181, 230, 29)
    highlight_surface = pygame.Surface((square_size, square_size))
    highlight_surface.fill(green_color)
    highlight_surface.set_alpha(100)
    colors = [white_color, black_color,
              highlight_surface]
    # The black square, white square images and highlight square images

    game_state = GameState()
    pieces_images = {}  # A dictionary with the chess piece notations as keys and the images as values
    promotions = ['B', 'N', 'R', 'Q']  # The pieces available for pawn promotion
    promotion_font = pygame.font.SysFont("Arial", 24)
    status_font = pygame.font.SysFont("Arial", 18)
    promotion_text = promotion_font.render("To which piece would you like to promote the pawn?", True, (255, 255, 255))

    load_images()
    moves = []  # Moves list will have a maximum length of two values as tuples containing the start square and the end
    # square

    valid_moves = []  # A list of lists containing valid moves as Move objects; check GameState.Move

    highlighted_squares = []
    get_valid_moves()
    while True:
        move_made = False
        for event in pygame.event.get():

            if event.type == pygame.QUIT:  # Checks if the game is still running
                exit()

            if event.type == pygame.MOUSEBUTTONDOWN:
                column = pygame.mouse.get_pos()[0] // square_size  # The column at which the user clicked
                row = pygame.mouse.get_pos()[1] // square_size  # The row at which the user clicked
                selected_square = (row, column)
                if row <= 7:
                    piece_selected = game_state.board[row][column]
                else:
                    piece_selected = "--"

                if game_state.pawn_promotion != ():  # If there is a pawn to be promoted
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
                    # selected is not white ie: "-" or "b", that is on the first click only.
                    # Or if it is the second click

                    moves.append(selected_square)
                    highlighted_squares.append(selected_square)

                    for valid_move in valid_moves:
                        if len(moves) == 1 and valid_move.start_square == selected_square:
                            # Adds the valid moves of the selected piece to the highlighted squares if the
                            # selected square is a start_square in a Move object in the valid_moves list
                            highlighted_squares.append(valid_move.end_square)

                    if (selected_square == moves[0] and len(moves) == 2) \
                            or (piece_selected == "--" and len(moves) == 1):
                        # If the user selected the same piece in the second move or selected an empty square in the
                        # first move
                        moves = []  # Reset the moves list
                        highlighted_squares = []

                    elif len(moves) == 2 and Move(moves[0], moves[1]) in valid_moves:
                        # If the user picked a valid square at the second click
                        game_state.make_move(Move((moves[0]), (moves[1])))
                        moves = []
                        highlighted_squares = []
                        move_made = True
                        valid_moves = []

                    elif len(moves) == 2 and [moves[0], moves[1]] not in valid_moves:  # If the user didn't pick a valid
                        # square at the second click
                        moves = []
                        highlighted_squares = []

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_z:
                    game_state.undo_move()
                    move_made = True

        pygame.display.flip()  # updates the screen
        if move_made:
            get_valid_moves()
            move_made = False
        draw_board()
        if game_state.pawn_promotion == ():
            draw_pieces(game_state)
