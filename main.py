import pygame


def draw_board():
    for r in range(squares):
        for c in range(squares):
            # Picks either the white square or the black one
            color = colors[(r + c) % 2]
            screen.blit(color, pygame.Rect(r * square_size, c *
                                           square_size, square_size, square_size))  # Adds the
            # picked square


# Images are named in the format 'w' or 'b' for white or black + {the symbol of the piece} + '.png'
def draw_pieces():
    for r in [0, 1, 6, 7]:
        if r == 7:  # First row is white
            first = "w"
        elif r == 0:  # Last row is black
            first = "b"

        elif r in [6, 1]:  # For the rows containing pawns
            if r == 6:  # 2nd row is white
                first = "w"
            else:  # 7th row is black
                first = "b"
            piece = pygame.image.load(
                "Images/" + first + "P.png")  # Loads the pawn image
            piece_resized = pygame.transform.scale(
                piece, (square_size, square_size))
            for c in range(squares):  # Adds the pawn image to each column
                screen.blit(piece_resized, pygame.Rect(
                    c * square_size, r * square_size, square_size, square_size))
            continue

        else:
            continue
        # This is reached when r is in [0, 7], ie: the rows containing other pieces than pawns
        for c in range(squares):
            # Picks the piece from the pieces list according to the column
            second = pieces[c]
            piece = pygame.image.load("Images/" + first + second + ".png")
            piece_resized = pygame.transform.scale(
                piece, (square_size, square_size))
            screen.blit(piece_resized, pygame.Rect(c * square_size,
                                                   r * square_size, square_size, square_size))


if __name__ == "__main__":
    pygame.init()
    width = height = 512  # Game will run at 512 x 512
    screen = pygame.display.set_mode((width, height))
    # The black square and the
    colors = [pygame.image.load("Images/White.png"),
              pygame.image.load("Images/Black.png")]
    # white square images
    squares = 8
    square_size = height // squares
    pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    draw_board()
    draw_pieces()
    while True:
        for event in pygame.event.get():  # Checks if the game is still running
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()  # updates the screen
