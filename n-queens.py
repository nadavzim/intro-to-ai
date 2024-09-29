import random
impr = 0
def threats(board):
    # returns number of threats in board
    count = 0
    for i in range(0, len(board) - 1):
        for j in range(i + 1, len(board)):
            if board[i] == board[j] or abs(i - j) == abs(board[i] - board[j]):
                count = count + 1
    return count


def rndboard(x):
    # returns a board x*x with queens in random cols
    board = []
    for i in range(x):
        board.append(random.randrange(x))
    return board


def printboard(board):
    # prints the board: #= empty cell Q=a queen
    print()
    for r in range(len(board)):
        for c in range(len(board)):
            if board[r] == c:
                print('Q', end='')
            else:
                print('#', end='')
        print()
    return


def improve(board):
    global impr
    # improves board if improvment is possible,
    # returns num of threats in the board
    minimum = threats(board)
    improved = [0, board[0]]  # improved holds the best move
    for r in range(len(board)):
        tmp = board[r]
        for c in range(len(board)):
            impr += 1
            print(impr)
            board[r] = c
            x = threats(board)
            if x < minimum:
                minimum = x
                improved = [r, c]
        board[r] = tmp
    board[improved[0]] = improved[1]
    return minimum


def solve(size):
    r = 0
    impr =0
    # solves the (size) quenns problem
    b = rndboard(size)
    n = threats(b)
    while n > 0:
        print(r, impr)
        x = improve(b)
        if x == n:
            b = rndboard(size)
            r = r+1
            n = threats(b)
        else:
            n = x
    printboard(b)


solve(30)

