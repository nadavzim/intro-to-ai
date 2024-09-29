###########################################################################################
# ai adversary games - minimax algorithm                                                   #
# nadav zimmerman and ynon haiyon                                                          #
#                                                                                          #
# #  חשוב לנו לומר כי ניסינו מספר רב של יוריסטיקות מגוונת  כולל בדיקת המשקלים השונים של כל מאפיין
# #                  עד למציאת היוריסטקה הנוכחית, בה נראה כי המחשב בצורה המיטבית שלהצלחנו למצוא.
#  #       ניתן לראות כי היוריסטיקה עובדת טוב על רוב המקרים ומביאה לניצחון של המחשב ברוב המקרים.
###########################################################################################
"""
תשובה לשאלה 1 בהנחיות התרגיל:
השחקן השני מנצח.
כל שחקן בתורו בוחר אם הוא מוחק קוביה אחת או שורה שלימה (שתי משבצות), השחקן השני יגיב בדיוק באופן סימטטרי ובכך ינצח את המשחק:
במקרה בו השחקן  הראשון יוריד קוביה למשל (1,1), השחקן השני יוריד את הקוביה הנגדית (2,2),
כך יוותרו שתי קוביות לא באותה השורה – לא משנה מה יבחר השחקן הראשון השחקן השני יוריד את הקוביה הנותרת ובכך ינצח.
במקרה בו השחקן הראשון יוריד שורה שלימה השחקן השני יוריד את השורה הנותרת וינצח במשחק.
"""

import copy

VIC = 10 ** 20  # The value of a winning board (for max)
LOSS = -VIC  # The value of a losing board (for max)

SIZE = 4  # The board is SIZE X SIZE

'''
The state of the game is represented by a list of 2 items:
0. The game board - a matrix (list of lists) of strings. 
   An empty cell = space and an occupied cell = #
1. Who's turn is it: "Human" or "Computer"
'''


def create():
    # Returns an empty board. The human plays first.
    board = []
    for i in range(SIZE):
        board = board + [SIZE * ["#"]]
    return [board, "Human"]


def value(s):
    """Returns the value of the current state s
    The value is: VIC if the computer wins, LOSS if the computer loses,
    otherwise the func return the heuristic value of the board for intermediate states.
    the value is calculated by the heuristic function with the following parameters:
    1. full_row - the number of full rows in the board
    2. full_col - the number of full columns in the board
    3. central_squares - the number of central squares in the board
    4. corner_control - the number of corner squares in the board
    5. isolated_squares - the number of isolated squares in the board
    6. same_line_score - the score of the '#' in the same row or col
    7. score - the sum of the above parameters with the following weights:
        1 * (full_row + full_col) + 5 * central_squares + corner_control - isolated_squares - edge_control - remaining_squares
    the logic of this hurictic is that if all the '#' in the same row or col the game will wnd in the next turn,
    which the most important thing. and the other parameters are to direct the computer to the best move.
    soch as the central squares squares important squares in the board a
    """
    # Returns the heuristic value of s
    if isFinished(s):
        if s[1] == "Human":
            return VIC
        else:
            return LOSS

    same_line_score = all_in_same_line(s)  # if the '#' in the same row or col return 1000 - else 0
    if same_line_score != 0:
        return same_line_score # if the '#' in the same row or col the game will end in the next turn

    remaining_squares = sum(row.count('#') for row in s[0])
    full_row = sum([1 for row in s[0] if all(square == '#' for square in row)])  # count the full rows
    full_col = sum([1 for col in zip(s[0]) if all(square == '#' for square in col)])  # count the full cols
    edge_control = sum(1 for i in range(SIZE) for j in range(SIZE) if s[0][i][j] == '#' and (i in {0, SIZE - 1} or j in {0, SIZE - 1}))
    corner_control = sum(1 for i in {0, SIZE - 1} for j in {0, SIZE - 1} if s[0][i][j] == '#')

    central_squares, isolated_squares = 0, 0

    for i in range(SIZE):
        for j in range(SIZE):
            if s[0][i][j] == '#':
                if abs(i - SIZE // 2) <= 1 and abs(j - SIZE // 2) <= 1:
                    central_squares += 1
                if (i > 0 and s[0][i - 1][j] != '#') and (i < SIZE - 1 and s[0][i + 1][j] != '#') and \
                        (j > 0 and s[0][i][j - 1] != '#') and (j < SIZE - 1 and s[0][i][j + 1] != '#'):
                    isolated_squares += 1
    score = full_row + full_col + 5 * central_squares + corner_control - isolated_squares - edge_control - remaining_squares

    if s[1] == "Human":
        return - score
    return score


def all_in_same_line(s):
    """if the '#' in the same row or col return 1000 - else 0
    the logic of this function is that if all the '#' in the same row or col the game will wnd in the next turn,
    which means that the state is a terminal state and the value of the state is 1000 for the computer (max)
    or -1000 for the human (min)."""
    exists = []
    for i1 in range(SIZE):
        for j1 in range(SIZE):
            if s[0][i1][j1] == '#':
                exists.append([i1, j1])  # save the index of the '#'
                for i2 in range(SIZE):
                    for j2 in range(SIZE):
                        if s[0][i2][j2] == '#':
                            if i1 != i2 and j1 != j2:  # if there is two '#' not in the same col or row
                                return 0

    if len(exists) > 1:  # if there is at least two '#' in the same row or col
        r1, c1 = exists[0]  # get the first index of the '#'
        r2, c2 = exists[-1]  # get the last index of the '#'
        if r1 == r2:  # if the '#' in the same row
            for i in range(c1 + 1, c2):  # check if the '#' in the row aren't separated
                if s[0][r1][i] != '#':
                    return 0  # if the '#' in the row are separated
        elif c1 == c2:  # if the '#' in the same col
            for i in range(r1 + 1, r2):  # check if the '#' in the col aren't separated
                if s[0][i][c1] != '#':
                    return 0  # if the '#' in the col are separated
    if s[1] == "Human":
        return -1000
    else:
        return 1000


def printState(s):
    # Prints the board.
    for r in range(SIZE):
        print("abcdefghij"[r], end="")
        for c in range(SIZE):
            print(s[0][r][c], end="")
            if s[0][r][c] == "+":  # + indicates the computer's move
                s[0][r][c] = " "  # change to space after printing
        print()
    print(" 0123456789"[:SIZE + 1])

    if isFinished(s):
        if s[1] == "Human":
            print("I won.")
        else:
            print("You won.")


def isFinished(s):
    # Returns True iff the game ended
    for r in range(SIZE):
        for c in range(SIZE):
            if s[0][r][c] == "#":
                return False
    return True


def isHumTurn(s):
    # Returns True iff it the human's turn to play
    return s[1] == "Human"


def whoIsFirst(s):
    # The user decides who plays first
    if input("Who plays first? 1-me / anything else-you. : ") == "1":
        s[1] = "Computer"
    else:
        s[1] = "Human"


def inputMove(s):
    # Reads, enforces legality and executes the user's move.
    printState(s)
    flag = True
    while flag:
        move = input("The form of a single place is row and col without space (e.g. a1)\n\
        and for a range is row and col of the beginning and row and col for the end without space (e.g. a1a3)\n\
        Enter your next move: ")
        flag = not isLegal(s, move, " ")


def getNext(s):
    # returns a list of the next states of s
    ns = []
    for r in range(SIZE):
        for c in range(SIZE):
            c1 = c
            st = copy.deepcopy(s)
            if st[1] == "Human":
                st[1] = "Computer"
                # x is the sign for cards taken at the current move
                x = " "
            else:
                st[1] = "Human"
                x = "+"
            while c1 < SIZE and st[0][r][c1] == "#":
                st[0][r][c1] = x
                ns += [copy.deepcopy(st)]
                c1 += 1
            r1 = r
            st = copy.deepcopy(s)
            if st[1] == "Human":
                st[1] = "Computer"
                x = " "
            else:
                st[1] = "Human"
                x = "+"
            while r1 < SIZE and st[0][r1][c] == "#":
                st[0][r1][c] = x
                if r1 > r:  # To prevent multiplications
                    ns += [copy.deepcopy(st)]
                r1 += 1
    return ns


##############################################
# Check if move is legal in state s and if so will put x in the new empty cell/s
def isLegal(s, move, x):
    """The function check if the move is legal in the state s.
    The move is legal if: the move is in the board, the move is in one row or col or part of it,
     the move isn't taken and so on ...
     if the move is legal the function will delete the '#' in the input cell/s and return True.
    else the function will print the reason and return False."""
    invalid = False
    try:
        r1 = "abcdefghij".index(move[0])
        c1 = int(move[1])
        r2 = "abcdefghij".index(move[2])
        c2 = int(move[3])

    except IndexError:  # if the form is single place (e.g. a1)
        r2, c2 = r1, c1
    except ValueError:
        invalid = True

    #  check if the move is invalid - not (e.g b2d2) and so...
    if invalid or r1 not in range(SIZE) or r2 not in range(SIZE) or c1 not in range(SIZE) or c2 not in range(SIZE + 1):
        print("\nInvalid input, please try agin with valid input")
        return False
    # check if the move isn't row or col
    if c1 != c2 and r1 != r2:
        print("\nThe move is illegal, try another move")
        return False
    # check if part of the move already delete
    for r in range(min(r1, r2), max(r1, r2) + 1):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            if s[0][r][c] in [' ', '+']:
                print("\nThe move is taken, try another move")
                return False

    for r in range(min(r1, r2), max(r1, r2) + 1):
        for c in range(min(c1, c2), max(c1, c2) + 1):
            s[0][r][c] = x  # put '' in the new empty cell/s
    if s[1] == "Computer":
        s[1] = "Human"
    else:
        s[1] = "Computer"
    return True
