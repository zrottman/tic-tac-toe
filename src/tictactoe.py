import os

class Board:
    '''
    A class representing the tictactoe board.

    Attributes:
        board (list[str]): A list of length 9 representing a 3x3 matrix.
        WINNERS (list): A constant containing binary encodings of the 8
            winning board permutations.

    Methods:
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
        self.board = [' ',' ',' ',' ',' ',' ',' ',' ',' ']
        self.WINNERS = [
            0b111000000, 0b000111000, 0b000000111, 0b100100100,
            0b010010010, 0b001001001, 0b100010001, 0b001010100
        ]


    def __str__(self):
        '''
        String function that returns pretty formatted version of self.board.
        '''
        out = '   |   |   \n'
        row_start = 0 # Pointer to keep track of where each row starts
        rows = []

        # Separate `self.board` list into three rows 
        while row_start < len(self.board):
            rows.append(' ' + ' | '.join(self.board[row_start:row_start + 3]) + ' \n')
            row_start += 3

        # Join rows
        out += '___|___|___\n   |   |   \n'.join(rows)
        out += '   |   |   \n'
        
        return out


    def _encode_board(self, player_token):
        '''
        Helper function to encode `self.board` as a integer encoding
        from a binary encoding.

        Parameters:
            player_token (str): Player token (e.g., 'X' or 'O') to use to 
                encode `self.board`

        Returns:
            Int : Integer equivalent of binary encoding of board position for
                player indicated by `player_token`
        '''
        # Initialize output string with binary prefix
        binseq = '0b'

        # Loop through `self.board` and produce binary encoding for `player_token`
        for char in self.board:
            if char == player_token:
                binseq += '1'
            else:
                binseq += '0'

        # Return integer equivalent of binary encoding
        return int(binseq, 2)


    def is_winner(self, player_token):
        '''
        Determines whether `self.board` is a winner for player with `player_token`.
        
        Parameters:
            player_token (str): Player token to pass to `self._encode_board()`

        Returns:
            Bool: True if `self.board` is a winner for given `player_token`,
                else False.
        '''
        for winner in self.WINNERS:
            if winner & self._encode_board(player_token) == winner:
                return True
        return False


    def is_stalemate(self, player_tokens):
        '''
        Determines whether game has reached stalemate using bitwise operations.
        For each player, checks if that player's current board position plus
        all unoccupied spaces matches a potential winner in `self.WINENRS`.

        Parameters:
            player_tokens (List): list of player tokens

        Returns:
            Bool: True if self.board can't be a winner for either player
        '''
        for player_token in player_tokens:
            for winner in self.WINNERS:
                if (self._encode_board(player_token) | self._encode_board(' ')) & winner in self.WINNERS:
                    return False 
        return True


    def _is_valid_coord(self, coords):
        '''
        Helper function to validate `coords` tuple.

        Parameters:
            coords (tuple)

        Returns:
            Boolean: True if `coords` values are integers between [0, 3)
        '''
        
        row, col = coords
        if (type(row) != int) or (type(col) != int):
            return False
        if (row < 0) or (row > 2) or (col < 0) or (col > 2):
            return False
        return True


    def _is_unoccupied(self, coords):
        '''
        Helper function to validate whether target coordinates are unoccupied.

        Parameters:
            coords (tuple): (row, column)

        Returns:
            Boolean: True if `coord` position is empty, else False
        '''

        return self.board[self._coords_to_index(coords)] == ' '


    def _coords_to_index(self, coords):
        '''
        Helper function to return index of `self.board` based on (row, col)
        coords.

        Parameters:
            coords (tuple): (row, column)

        Returns:
            int: Index 0-8
        '''
        row, col = coords
        return row * 3 + col
        

    def update_board(self, player_token, coords):
        '''
        Function to update board at `coords` for player indicated by 
        `player_token`. Returns True if successful; returns False otherwise
        (e.g., if that position is invalid).

        Parameters:
            player_token (str): Player token
            coords (tuple): Format (row, column)

        Returns:
            Bool: True if update was successful; false if position was invalid.
        '''

        if self._is_valid_coord(coords) and self._is_unoccupied(coords):
            self.board[self._coords_to_index(coords)] = player_token
            return True
        else:
            return False


class Game:
    '''
    A class to represent the game. Contains a board object and players objects.
    '''

    def __init__(self):
        self.players = []
        self.board = Board()
        self.move_count = 0

    def run_game(self):
        
        # Create 2 default players
        self.players.extend([Player('player1', 'X'), Player('player2', 'O')])

        # Game loop 
        while True:

            os.system('clear')
            
            # Display board
            print('\n-------------------------\n')
            print(self.board)

            # Prompt current player for a move and validate
            while True:
                print("\n{} is up".format(self.get_current_player_name()))
                cur_row = int(input("Row? "))
                cur_col = int(input("Col? "))

                if self.board.update_board(self.get_current_player_token(), (cur_row, cur_col)):
                    break
                else:
                    print("Error, please try again")

            # If `self.move_count` >= 4, check if game is over
            if self.move_count >= 4:
                
                # Check to see if current player won. If so, break
                if self.board.is_winner(self.get_current_player_token()):
                    print("{} won! Game over".format(self.get_current_player_name()))
                    break

                # Check if stalemate. If so, break.
                elif self.board.is_stalemate(self.get_player_tokens()):
                    print("Stalemate. Game over.")
                    break

            self.move_count += 1

    def get_player_tokens(self):
        return [player.token for player in self.players]

    def get_current_player(self):
        return self.players[self.move_count % 2]

    def get_current_player_token(self):
        return self.get_current_player().get_token()

    def get_current_player_name(self):
        return self.get_current_player().get_name()


class Player:
    '''
    A class to represent each player. Contains player token and name.
    '''

    def __init__(self, name, token):
        self.name = name
        self.token = token

    def get_token(self):
        return self.token

    def get_name(self):
        return self.name


if __name__ == '__main__':
    
    mygame = Game()

    mygame.run_game()
    
