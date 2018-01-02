#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 23 16:06:59 2017

@author: hiroyukiinoue
"""

class Player:
    """
    Handles the state of the player.

    Attributes:
        idx (int)          : player ID. either 1 or 2.
        num_soldiers (int) : number of remaining soldiers.
        coordinates (list) : list of tuples that records the coordinates of
                             remaining soldiers.
    """
    def __init__(self, player_id):
        self.idx = player_id
        self.num_soldiers = 0
        self.coodinates = set()

    def count_soldiers(self):
        """ Returns the number of remaining soldiers."""
        return self.num_soldiers

    def add_soldier_coodinate(self, coord):
        """
        Adds a coodinate of the friend soldier.

        Args:
            coord : len = 2. tuple. x, y coodinate.

        Returns:
            None.
        """
        assert isinstance(coord, tuple), 'pass a tuple of the coordinate.'
        assert len(coord) == 2, 'it should be a 2d coordinate.'
        self.coodinates.add(coord)
        self.num_soldiers += 1

    def remove_soldier_coodinate(self, coord):
        """
        Removes the coodinate of the friend soldier.

        Args:
            coord : len = 2. tuple. x, y coodinate.

        Returns:
            None.
        """
        assert isinstance(coord, tuple), 'pass a tuple of the coordinate.'
        assert len(coord) == 2, 'it should be a 2d coordinate.'
        assert coord in self.coodinates, "No soldier at this coordinte."
        self.coodinates.remove(coord)
        self.num_soldiers -= 1

    def get_soldier_coodinates(self):
        """ Returns all the coodinates of the remaining soldiers."""
        return self.coodinates


class Checker:
    """
    Plays Checker by handling the state of the board, verifying the moves of
    the soldiers and updating the Player instances.

    Attributes:
        board (list)     : records the state of 8 x 8 baord.
                           0  : represents "unoccupied"
                           1  : represents "player1's soldier"
                           2  : represents "player2's soldier"
                           '' : represents forbidden space.
        palyer1 (Player) : player1 as an instance of Pleyer class.
        palyer2 (Player) : player2 as an instance of Pleyer class.
        moves (list)     : records the moves loaded from the file.
        num_step (int)   : number of steps in the moves. len(moves).
    """
    def __init__(self):
        self.board = None
        self.player1 = Player(1) #white
        self.player2 = Player(2) #black
        self.moves = []
        self.num_steps = 0

    def initialize_board(self):
        """
        Generates a 8 x 8 grid board for checkers. As we only play with 8 x 8, we
        don't introduce an argument to get a userinput for the number of grid.
        Args:

        Intermediate:

        Returns:
            board : list. (8, 8)
                    0 : represents "unoccupied"
                    1 : represents "player1's soldier"
                    2 : represents "player2's soldier"
        """
        board = [['' for x in range(8)] for y in range(8)]
        for j in range(0, 3):
            for i in range((j+1)%2, 8, 2):
                board[i][j] = 1
                self.player1.add_soldier_coodinate((i, j))
        for j in range(5, 8):
            for i in range((j+1)%2, 8, 2):
                board[i][j] = 2
                self.player2.add_soldier_coodinate((i, j))
        for j in range(3, 5):
            for i in range((j+1)%2, 8, 2):
                board[i][j] = 0
        self.board = board

    def load_moves(self, file):
        """
        Loads the specified movement file.

        Args:
            file : must be among 'white', 'black', 'illegal' and 'incomplete'.

        Returns:
            moves : list of tuples of initial positions and final positions.
        """
        if file == 'white':
            path = './white.txt'
        elif file == 'black':
            path = './black.txt'
        elif file == 'incomplete':
            path = './incomplete.txt'
        elif file == 'illegal':
            path = './illegal_move.txt'
        else:
            raise "such file does not exist. Must be among 'white', 'black'\
                  , 'illegal' and 'incomplete'."
        moves = []
        with open(path) as lines:
            for line in lines:
                x_i, y_i, x_f, y_f = line.split(',')
                moves.append((int(x_i), int(y_i), int(x_f), int(y_f)))
        self.moves = moves
        return moves

    def check_valid_move(self, move, player_id):
        """
        Checks if this specified move is possible.

        Args:
            move   :   final position. tuple. len(move) = 4.

        Intermediate:
            p_i    : initial position. tuple. len(p_i) = 2.
            p_f    : final position. tuple. len(p_f) = 2.
            check1 : check if pf is within the board.
            check2 : check pf is a valid space if at all.
            check3 : check pf is a empty space.
            check4 : check pf is not the same as pi.
            check5 : check if the move is a forward move for the player.
            check6 : check if the move is not too large.
            check7 : check if the move is not just straightly forward.
            At this point, we are only left with possibilibilities of
                      only a simple step forward or a capture move.
            check8 : check if the move is a valid one step forward
            check9 : check if the move is a valid capture move.

        Returns:
            valid_move    : boolean. True if it's a valid move.
            valid_capture : dict.
                            ['bool'] = Flase
                            or
                            ['bool'] = True
                            ['prey'] = player1 or player2
                            ['coordiante'] = (x_mid, y_mid)
        """
        valid_move = False
        valid_capture = {'bool': False}
        p_i = move[:2]
        p_f = move[2:]
        if p_f[0] > 7 or p_f[1] > 7 or p_f[0] < 0 or p_f[1] < 0:
            return valid_move, valid_capture
        if self.board[p_f[0]][p_f[1]] == '':
            return valid_move, valid_capture
        if self.board[p_f[0]][p_f[1]] != 0:
            return valid_move, valid_capture
        if p_f[0] == p_f[0] and p_i[1] == p_f[1]:
            return valid_move, valid_capture
        if ((-1) ** (player_id + 1)) * (p_f[1] - p_i[1]) <= 0:
            return valid_move, valid_capture
        if abs(p_f[0] - p_i[0]) >= 3 or abs(p_f[1] - p_i[1]) >= 3:
            return valid_move, valid_capture
        if p_f[0] == p_i[0] or p_f[1] == p_i[1]:
            return valid_move, valid_capture
        if abs(p_f[0] - p_i[0]) == 1:
            assert (p_f[1] - p_i[1]) == (-1) ** (player_id + 1)
            valid_move = True
            return valid_move, valid_capture
        if abs(p_f[0] - p_i[0]) == 2:
            assert (p_f[1] - p_i[1]) == 2 * (-1) ** (player_id + 1)
            x_mid = int((p_f[0] + p_i[0])/2)
            y_mid = int((p_f[1] + p_i[1])/2)
            if self.board[x_mid][y_mid] == 3 - player_id:
                valid_move = True
                valid_capture['bool'] = True
                valid_capture['prey'] = 3 - player_id
                valid_capture['coordiante'] = (x_mid, y_mid)
                return valid_move, valid_capture
            else:
                raise "Invalid move. You cannot step over a friend."

    def update_board_with_new_move(self, move, turn, valid_capture):
        """
        update the board with the new move, given that the move's validity has
        been verified already.

        Args::
            p_i : initial position. tuple (2, ).
            p_f :   final position. tuple (2, ).

        Returns:
            None.
        """
        p_i = move[:2]
        p_f = move[2:]
        self.board[p_i[0]][p_i[1]] = 0
        self.board[p_i[0]][p_i[1]] = 0
        self.board[p_f[0]][p_f[1]] = turn.idx
        self.board[p_f[0]][p_f[1]] = turn.idx
        turn.remove_soldier_coodinate(p_i)
        turn.add_soldier_coodinate(p_f)
        if valid_capture['bool'] is True:
            x_mid = int((p_i[0] + p_f[0])/2)
            y_mid = int((p_i[1] + p_f[1])/2)
            valid_capture['coordinate'] = (x_mid, y_mid)
            self.board[x_mid][y_mid] = 0
            if valid_capture['prey'] == 1:
                self.player1.remove_soldier_coodinate((x_mid, y_mid))
            else:
                self.player2.remove_soldier_coodinate((x_mid, y_mid))

    def check_any_valid_moves_this_turn(self, player):
        """
        Checks if there is any possible move for the current player for the
        current board state.

        Args:
            player : the current player

        Intermediate:
            x_c     : x coordinate of the solder under concern.
            y_c     : y coordinate of the solder under concern.
            sgn     : forward for this current player.
            one_pos : check if moving +1 in x (and sgn in y) is invalid.
            one_neg : check if moving -1 in x (and sgn in y)is invalid.
            two_pos : check if moving +2 in x (and 2 * sgn in y) is invalid.
            one_pos : check if moving -2 in x (and 2 * sgn in y)is invalid.

        Returns:
            answer  : boolean. True if any possible move for the player.
        """
        answer = False
        for coord in player.get_soldier_coodinates():
            y_c, x_c = coord
            sgn = (-1) ** (player.id + 1)
            one_pos = True
            one_neg = True
            two_pos = True
            two_neg = True
            if x_c + 1 <= 7 and  y_c + sgn <= 7 and y_c + sgn >= 0:
                one_pos = self.board[x_c + 1][y_c + sgn] != 0
            if x_c - 1 >= 0 and  y_c + sgn <= 7 and y_c + sgn >= 0:
                one_neg = self.board[x_c - 1][y_c + sgn] != 0
            if x_c + 2 <= 7 and  y_c + 2 * sgn <= 7 and y_c + 2 * sgn >= 0:
                two_pos = self.board[x_c + 2][y_c + 2 * sgn] != 0 or \
                          (self.board[x_c + 2][y_c + 2 * sgn] == 0 and \
                           self.board[x_c + 1][y_c + sgn] == player.id)
            if x_c - 2 >= 0 and  y_c + 2 * sgn <= 7 and y_c + 2 * sgn >= 0:
                two_neg = self.board[x_c - 2][y_c + 2 * sgn] != 0 or \
                          (self.board[x_c - 2][y_c + 2 * sgn] == 0 and \
                           self.board[x_c - 1][y_c + sgn] == player.id)
            if not (one_pos and one_neg and two_pos and two_neg):
                answer = True
                break
        return answer

    def report_result(self):
        """
        Reports the result of this game.

        Args:
            None.

        Returns:
            None.
            print the result according to the remaining soldiers of both sides.
        """
        if self.player1.count_soldiers() > self.player2.count_soldiers():
            print('first')
        elif self.player1.count_soldiers() < self.player2.count_soldiers():
            print('second')
        else:
            print('tie')

    def print_board(self, step, idx, move):
        """
        Print the state of the board for a sanity check.

        Args:
            step : current step.
            idx  : player's id
            move : this move. tuple. len(move) = 4

        Returns:
            None.
            print the result according to the remaining soldiers of both sides.
        """
        print('step {}, player{}, move = {}'.format(step, idx, move))
        for line in self.board:
            print(line)
        print('')

    def play_this_turn(self, move, turn, step):
        """
        play this turn for the current player.

        Args:
            move : this move. tuple. len(move) = 4
            turn : either self.player1 or self.player2
            step : current step.

        Returns:
            stop : 0 if the game should stop. 1 otherwise.
            step : current step after this player's turn.
        """
        idx = turn.idx
        valid_move, valid_capture = self.check_valid_move(move, idx)
        if valid_move and valid_capture['bool']:
            self.update_board_with_new_move(move, turn, valid_capture)
            while True and step < self.num_steps - 1:
                try_move = self.moves[step + 1]
                valid_move, valid_capture = self.check_valid_move(try_move, idx)
                if valid_move and valid_capture['bool']:
                    self.update_board_with_new_move(try_move, turn, valid_capture)
                    #self.print_board(step, turn.id, try_move)
                    step += 1
                else:
                    break
        elif valid_move and not valid_capture['bool']:
            self.update_board_with_new_move(move, turn, valid_capture)
        else:
            stop = 0
            illegal = 1
            print('illegal_move.txt - line {} illegal move: {}, {}, {}, {}'.\
                  format(step + 1, move[0], move[1], move[2], move[3]))
            return stop, step, illegal
        stop = 1
        illegal = 0
        return stop, step, illegal

    def play_checker(self, file):
        """
        main function of Checker.

        Args:
            file : should be among 'white', 'black', 'illegal' and 'incomplete'

        Returns:
            None : print the result.
        """
        self.initialize_board()
        moves = self.load_moves(file)
        self.num_steps = len(moves)
        turn = self.player1
        step = 0
        stop = 1
        illegal = 0
        while stop != 0 and step < self.num_steps:
            move = moves[step]
            if turn == self.player1:
                stop, step, illegal = self.play_this_turn(move, turn, step)
                #self.print_board(step, turn.id, move)
                turn = self.player2
            else:
                stop, step, illegal = self.play_this_turn(move, turn, step)
                #self.print_board(step, turn.id, move)
                turn = self.player1
            step += 1
        if self.check_any_valid_moves_this_turn(turn) and illegal != 1:
            print('incomplete.txt - incomplete game')
            return
        elif illegal != 1:
            self.report_result()
            return

def main(file):
    """
    Play Checker.

    Args:
        file : should be among 'white', 'black', 'illegal' and 'incomplete'

    Returns:
        None. print the result.
    """
    Checker().play_checker(file)

if __name__ == "__main__":
    main('white')
    #main('black')
    #main('illegal')
    #main('incomplete')
