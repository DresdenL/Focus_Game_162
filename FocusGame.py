# Author: Dresden Lee
# Date: 11/26/2020
# Description: Program that represents a game called "Focus". Has three classes: FocusGame, Board, and Player.
# This program has the appropriate methods for playing an entire game, including winning messages,
# checking for legal turns, etc.

class FocusGame:
    """
    FocusGame is the main class and it interacts with the other two classes
    (player and board) using composition. A FocusGame has a board and has
    players. When a FocusGame object is created, the FocusGame initialises the
    two players as Player objects, creates it's Board object, and
    initializes the board with colors at appropriate positions. FocusGame has to
    communicate with the Player class and Board class when moving pieces on the board,
    adding pieces to a players reserves or captured pile, and changing a players turn.
    """

    def __init__(self, first_player, second_player):
        """
        focus game init method.
        Method takes two tuples as parameters. Each tuple has a player name
        and color. The method initialises player1 and player2
        as Player objects using the values in the tuples.
        Method sets the board as a Board object and then fills in the
        starting values on the board using Board's set_board() method.
        """
        self._player1 = Player(first_player[0], first_player[1])
        self._player2 = Player(second_player[0], second_player[1])
        self._gameboard = Board()
        self._gameboard.set_board(first_player[1], second_player[1])

    def get_current_board(self):
        """This method calls get_board of the Board class.
        It returns the board."""
        return self._gameboard.get_board()

    def show_pieces(self, position):
        """
        Position is a tuple parameter containing (row, column).
        This function returns the piece(s) (if any)
        located at that position. It calls the boards show_board_position
        function.
        """
        return self._gameboard.show_board_position(position)

    def get_player_from_name(self, player_name):
        """
        This method returns the player object matched to the player_name
        passed as a parameter.
        """
        if self._player1.get_name() == player_name:
            return self._player1
        elif self._player2.get_name() == player_name:
            return self._player2
        else:
            return False

    def show_reserve(self, player_name):
        """
        This function takes a players name as a parameter and returns their reserves.
        """

        the_player = self.get_player_from_name(player_name)
        return the_player.get_reserves()

    def show_captured(self, player_name):
        """Method takes player's name as a parameter. Method
        matches the players name to a player object, then returns the player
        object's captured (integer value >= 0) using
        get_captured method in Player class.
        I am considering adding a condition that returns an error
        message if player_name is not matched to an object."""

        the_player = self.get_player_from_name(player_name)
        return the_player.get_captured()

    def check_legal(self, player_name, current_position, new_position, num_pieces_moved):
        """
        The function checks that the move is legal (that the
        move is either horizontal or vertical an appropriate amount of spaces.)
        Players name, current position tuple, new position tuple, and
        number of pieces moved are passed as parameters.
        Illegal moves: Attempting to move a piece that is not their color.
        Attempting to move more pieces than are in the stack.
        Attempting to move off the board.
        Attempting to move x amount of pieces from stack to a location that is not
        = to x.
        """

        the_player = self.get_player_from_name(player_name)
        row_1 = current_position[0]
        column_1 = current_position[1]
        row_2 = new_position[0]
        column_2 = new_position[1]
        # current_stack = self._gameboard.show_board_position(current_position)

        # check if number of pieces the player is trying to move is less than or equal to the
        # list's length. If not, return "invalid number of pieces.
        #if len(current_stack) < num_pieces_moved:
            #return False

        # Check that they are moving piece to somewhere on board.
        if row_1 > 5 or row_2 > 5 or column_1 > 5 or column_2 > 5 or row_1 < 0 or row_2 < 0 or column_2 < 0\
                or column_1 < 0:
            return False

        current_stack = self._gameboard.show_board_position(current_position)
        if len(current_stack) < num_pieces_moved:
            return False
        # check that move is not diagonal.
        elif current_position[0] != new_position[0] and current_position[1] != new_position[1]:
            return False

        # vertical moves happen if the row is different/column is same
        # This is a vertical move. Make sure that the vertical move is correct spaces.
        elif row_1 != row_2:
            if row_1 - row_2 != num_pieces_moved and row_2 - row_1 != num_pieces_moved:
                return False
            else:
                return True

        # horizontal move. Check that is is an appropriate amount of spaces.
        elif column_1 != column_2:
            if column_1 - column_2 != num_pieces_moved and column_2 - column_1 != num_pieces_moved:
                return False
            else:
                return True

        else:
            return True

    def move_piece(self, player_name, current_position, new_position, num_pieces_moved):
        """
        This function takes player's name, current_position tuple, new
        position tuple, and number of pieces being moved as parameters.
        This function will call check_legal with those parameters.
        If check_legal returns True, this function will determine which move method to call
        in board class and then call that method.
        set_turn in Player class is called on both player objects to change their turns.
        check_stack is called. Check_win is called.
        """

        the_player = self.get_player_from_name(player_name)
        # try putting this in check legal
        # current_stack = self._gameboard.show_board_position(current_position)

        # neither player has gone yet, so either player may start.
        if self._player1.get_turn() is False and self._player2.get_turn() is False:
            the_player.set_turn()

        # check if it is players turn.
        if the_player.get_turn() is False:
            return False

        # check that its the player's piece/stack. (try putting this in check_legal)
        # elif current_stack[-1] != the_player.get_color():
            # return False

        elif self.check_legal(player_name, current_position, new_position, num_pieces_moved) is True:
            # single move
            current_stack = self._gameboard.show_board_position(current_position)
            if current_stack[-1] != the_player.get_color():
                return False
            elif len(current_stack) == 1:
                self._gameboard.single_move(current_position, new_position)
                self._player1.set_turn()
                self._player2.set_turn()
                self.check_stack(the_player, new_position)
                return self.check_win(the_player)
            # multiple move
            else:
                self._gameboard.multiple_move(current_position, new_position, num_pieces_moved)
                self._player1.set_turn()
                self._player2.set_turn()
                self.check_stack(the_player, new_position)
                return self.check_win(the_player)
        else:
            return False

    def reserved_move(self, player_name, location):
        """
        This function takes players name and location tuple
        as parameters. If it's not the players turn or
        player has no reserves, False is returned.
        Otherwise, reserve_move in Board class is called. Set_turn is called
        on both player objects. Check_stack is called. Check_win is called.
        """

        the_player = self.get_player_from_name(player_name)

        if the_player.get_turn() is not True:
            return False
        elif the_player.get_reserves() == 0:
            return False
        elif location[0] > 5 or location[1] > 5 or location[0] < 0 or location[1] < 0:
            return False
        else:
            self._gameboard.reserve_move(the_player, location)
            self._player1.set_turn()
            self._player2.set_turn()
            self.check_stack(the_player, location)
            return self.check_win(the_player)

    def check_stack(self, player_object, board_position):
        """"
        Takes player object and board position as parameters.
        If stack is > 5, check_stack will remove
        x pieces (x = len(position_list) - 5) from bottom of stack.
        inc_reserves is called on player_object if element being removed is
        player's color. inc_captured is called if element being removed is
        opponents color.
        """
        current_stack = self._gameboard.show_board_position(board_position)
        while len(current_stack) > 5:
            if current_stack[0] == player_object.get_color():
                player_object.inc_reserves()
                current_stack.remove(current_stack[0])
            else:
                player_object.inc_captured()
                current_stack.remove(current_stack[0])

    def check_win(self, player_object):
        """
        If get_captures >= 6, player won.
        Return win message.
        """
        if player_object.get_captured() >= 6:
            return player_object.get_name() + " Wins"
        else:
            return "successfully moved"


class Player:
    """
    Player class. This represents a player object with name,
    color, reserves counter, captured counter, and turn state.
    """

    def __init__(self, name, color):
        """a player has a name, color, a reserve pile, and a captured pile.
        The player's reserves and captured are initialized to 0. The players turn
        is set as False"""

        self._name = name
        self._color = color
        self._reserves = 0
        self._captured = 0
        self._turn = False    # False if not players turn, True if it is players turn

    def get_name(self):
        """returns player name"""
        return self._name

    def get_color(self):
        """returns player color"""
        return self._color

    def set_turn(self):
        """Changes the player's turn state."""

        if self._turn is False:
            self._turn = True
        else:
            self._turn = False

    def get_turn(self):
        """returns turn state of player"""
        return self._turn

    def inc_captured(self):
        """Increases player's captured pile by 1"""
        self._captured += 1

    def get_captured(self):
        """returns captured pile (# of pieces captured by player)"""
        return self._captured

    def inc_reserves(self):
        """increases player's reserve pile by 1"""
        self._reserves += 1

    def dec_reserves(self):
        """decreases 1 from player's reserves."""
        self._reserves -= 1

    def get_reserves(self):
        """returns player's reserved pile"""
        return self._reserves


class Board:
    """Object that represents a board with positions that are lists of lists.
    There are 6 rows and 6 columns. Each (row, column) position is a list."""

    def __init__(self):
        """
        Board starts out with initialized empty state.
        """
        row0 = [[] for x in range(0, 6)]
        row1 = [[] for x in range(0, 6)]
        row2 = [[] for x in range(0, 6)]
        row3 = [[] for x in range(0, 6)]
        row4 = [[] for x in range(0, 6)]
        row5 = [[] for x in range(0, 6)]

        self._board = [row0, row1, row2, row3, row4, row5]

    def single_move(self, tuple_start, tuple_end):
        """
        Takes tuple_start (starting position) and tuple_end (move position)
        as parameters.
        This method assumes that the move is legal.
        This moves single piece from current position's list and appends it to
        new position.
        """

        row = tuple_start[0]
        column = tuple_start[1]
        row2 = tuple_end[0]
        column2 = tuple_end[1]
        self._board[row2][column2].append(self._board[row][column][0])
        self._board[row][column].remove(self._board[row][column][0])

    def multiple_move(self, tuple_start, tuple_end, pieces_to_move):
        """
        Takes tuple_start (current position (row, column)),
        tuple_end (next position (row, column)), and
        pieces_to_move (integer value for how many pieces will go from
        old position to new position) as parameters.
        Method assumes that the move is legal. Append the last
        x amount of pieces to tuple_end position list. Then
        remove the last x amount of pieces from tuple_start position
        list. (where x = pieces_to_move. We are removing x amount
        of pieces from top of the stack at current position and
        adding those pieces to top of new position).
        """

        a_counter = 0  # will count how many pieces have been moved.
        current_stack = self.show_board_position(tuple_start)
        new_stack = self.show_board_position(tuple_end)
        el_to_move = len(current_stack) - pieces_to_move

        if len(current_stack) == pieces_to_move:
            for el in current_stack:
                new_stack.append(el)
            current_stack.clear()

        else:
            while a_counter < pieces_to_move:
                self._board[tuple_end[0]][tuple_end[1]].\
                    append(self._board[tuple_start[0]][tuple_start[1]][el_to_move])
                self._board[tuple_start[0]][tuple_start[1]].\
                    remove(self._board[tuple_start[0]][tuple_start[1]][el_to_move])
                a_counter += 1

    def reserve_move(self, player_object, position):
        """
        Called with player object and position (tuple) as parameters.
        Takes the player's piece and appends it to the position on the board.
        Then player's reserves are decreased by 1.
        """
        row = position[0]
        column = position[1]
        color = player_object.get_color()
        self._board[row][column].append(color)
        player_object.dec_reserves()

    def get_board(self):
        """returns board, with each row on a new line."""
        for each_list in self._board:
            print(each_list)

    def set_board(self, color1, color2):
        """
        Initializes board to starting state.
        Takes two colors as parameters.
        """
        for x in range(6):
            if (x % 2) == 0:
                self._board[x][0].append(color1)
                self._board[x][1].append(color1)
                self._board[x][2].append(color2)
                self._board[x][3].append(color2)
                self._board[x][4].append(color1)
                self._board[x][5].append(color1)
            else:
                self._board[x][0].append(color2)
                self._board[x][1].append(color2)
                self._board[x][2].append(color1)
                self._board[x][3].append(color1)
                self._board[x][4].append(color2)
                self._board[x][5].append(color2)

    def show_board_position(self, position):
        """
        Takes position tuple (row, column) as parameter.
        shows all pieces in stack at current position,
        which is represented as a list
        """
        row = position[0]
        column = position[1]
        return self._board[row][column]

