import pygame


def draw_board():
    for r in range(squares):
        for c in range(squares):
            color = colors[(r + c) % 2]
            screen.blit(color, pygame.Rect(r * square_size, c * square_size, square_size, square_size))


def draw_pieces():
    first = ''
    second = ''
    for r in range(squares):
        if r in [0, 1]:
            first = 'w'
        elif r in [6, 7]:
            first = 'b'
        for c in range(squares):
            pass


if __name__ == "__main__":
    pygame.init()
    width = height = 800
    screen = pygame.display.set_mode((width, height))
    screen.fill(pygame.Color("white"))
    colors = [pygame.image.load("Images/White.png"), pygame.image.load("Images/Black.png")]
    squares = 8
    square_size = height // squares
    for item in colors:
        pygame.transform.scale(item, (square_size, square_size))
    pieces = ['R', 'N', 'B', 'Q', 'K', 'B', 'N', 'R']
    draw_board()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        pygame.display.flip()
