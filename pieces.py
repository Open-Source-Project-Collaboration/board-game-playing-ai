class Pieces(object):
    def __init__(self, color, name, row, col):
        self.Color = color
        self.name = name
        self.row = row
        self.col = col


    def is_valid(self):
        if self.color == 'w':
            opponent_piece_color = 'b'
        else:
            opponent_piece_color = 'w'


    def pawn_moves(self):
        # White: next_row == row-1 ||| Black: next_row == row+1