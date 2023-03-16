class Board:
    '''
    A class representing the tictactoe board.

    Attributes:
        board (List[List[str]]): A 3x3 matrix, where the outer list
            represents rows and the inner list represents columns.
        WINNERS (List): A constant containing binary encodings of the 8
            winning board permutations.

    Methods:
        flatten (List): Returns flat list of `self.board` matrix
        encode (str): Returns binary encoding of `self.board` given
            player token parameter
        is_winner (bool): Returns True if binary encoding of `self.board` 
            matches self.WINNERS for given player token, else returns False.
    '''
    
    def __init__(self):
        '''
        Constructor function that initializes Board object with empty matrix
        and constant containing all winning board permutations.
        '''
        self.board = [[' ',' ',' '],[' ',' ',' '],[' ',' ',' ']]
        self.WINNERS = [
            0b111000000, 0b000111000, 0b000000111, 0b100100100,
            0b010010010, 0b001001001, 0b100010001, 0b001010100
        ]


    def __str__(self):
        '''
        String function that returns pretty formatted version of self.board.
        '''
        out = '   |   |   \n'
        rows = [' ' + ' | '.join(row) + ' \n' for row in self.board]
        out += '___|___|___\n   |   |   \n'.join(rows)
        out += '   |   |   \n'
        return out


    def flatten(self):
        '''
        Helper function to flatten `self.board` as List of length 9.

        Returns:
            List: length 9
        '''
        return [item for row in self.board for item in row]


    def encode(self, player_token):
        '''
        Helper function to encode flattened `self.board` as a integer encoding
        from binary encoding.

        Parameters:
            player_token (str): Player token (e.g., 'X' or 'O') to use to 
                encode `self.board`

        Returns:
            Int : Integer equivalent of binary encoding of board position for
                player indicated by `player_token`
        '''
        binseq = '0b'
        for char in self.flatten():
            if char == player_token:
                binseq += '1'
            else:
                binseq += '0'
        return int(binseq, 2)


    def is_winner(self, player_token):
        '''
        Helper function to determine whether `self.board` is a winner given
        `player_token`.
        
        Parameters:
            player_token (str): Player token to pass to `self.encode()`

        Returns:
            Bool: True if `self.board` is a winnder for given `player_token`,
                else False.
        '''
        for winner in self.WINNERS:
            if winner & self.encode(player_token) == winner:
                return True
        return False



if __name__ == '__main__':
    
    b = Board()
    b.board[0][1] = 'X'
    b.board[1][1] = 'O'
    b.board[0][0] = 'X'
    b.board[2][0] = 'O'
    b.board[0][2] = 'X'

    print("Flattened")
    print(b.flatten())

    print()
    print()
    print(b)

    print()
    print()
    print(b.encode('X'))
    print(b.encode('O'))

    print("X is winner? {}".format(b.is_winner('X')))
    print("Y is winner? {}".format(b.is_winner('Y')))
