import random as r

#Plays the chess puzzle game with an interactive script
def play():
    #Generate a random board of heads and tails
    b = auto_board()
    #Intro
    print("Welcome to the Prisoner's puzzle!")
    print("\n")
    print("If you would like to leave prison, you must solve this puzzle with a fellow inmate!")
    print("There will be an 8x8 board of coins heads or tails side up, chosen competely at random.")
    print("The Warden will hide a key under one of these coins.")
    print("The first prisoner will see where this key is hidden, but the second prisoner will not.")
    print("The first prisoner then MUST flip ONE coin and ONE coin ONLY.")
    print("The first prisoner will then leave the room without communicating at all with the second prisoner.")
    print("The second prisoner must then return to the board and guess the location of the Warden's key.")
    print("If the second prisoner is able to find the key, you are both free!...")
    print("...but if not, then you both return to your sentences.")
    print("\n")
    #Role assignments
    input("Are you ready to play? Press Enter to continue.")
    print("\n")
    print("You must play with 3 players: 1 Warden and 2 Prisoners.")
    print("Please select your roles now...")
    print("\n")
    warden = input("Who will be the Warden? ")
    p1 = input("Who will be the coin flipping Prisoner? ")
    p2 = input("Who will be the key finding Prisoner? ")
    #Second prisoner leaves room
    input(p2 + ", please leave the room. Hit Enter to proceed once " + p2 + " has left.")
    print("\n\n")
    print_board(b)
    print("\n")
    print("Ok, now that " + p2 + " is gone, we can begin... ")
    print("\n")
    #Warden hides the key
    message = "Please type the number corresponding to your desired location on the board and hit enter. "
    key = input(warden + ", where would you like to hide the key? " + message)
    #First prisoner flips the coin
    f = input(p1 + ", which coin would you like to flip? " + message)
    b = flip(b, int(f))
    #First prisoner leaves, second prisoner returns
    print(p1 + ", please leave the room and " + warden + ", please tell " + p2 + " to come back to guess.")
    input("Hit Enter to continue.")
    print("\n\n")
    print_board(b)
    print("\n")
    #Second prisoner guesses
    guess = input(p2 + ", which location do you believe the key is in? ")
    print("\n")
    #Computer's guess
    input("The computer has a guess of its own! Hit Enter to find out what the computer thinks...")
    comp_ans = str(solve(b))
    print("The computer's guess using the optimal solution would have been: " + comp_ans)
    assert comp_ans == key, "The computer is incorrect?!? Something is very wrong..."
    input("Hit Enter to see if the key finding prisoner was right!")
    #Did the Warden or prisoners win?
    if guess == key: #Prisoners win
        print("Congratulations! You found the key and can now be free! Even the computer agrees!")
    else: #Warden wins
        print("Oh no! You didn't find the key! You will not be leaving prison today!")
    print("Thank you for playing!")
    return

#Auto generate a board of randomly heads and tails coins
def auto_board():
    board = [[0 for j in range(8)] for i in range(8)]
    headstails = ['H', 'T']
    for i in range(8):
        for j in range(8):
            board[i][j] = headstails[r.randint(0, 1)]
    return board

#Print board
def print_board(board):
    for i in range(8):
        rowstr = ""
        numstr = ""
        for j in range(8):
            rowstr += board[i][j]
            n = 8 * i + j
            numstr += str(n)
            if j != 7:
                rowstr += " "
                if n < 10:
                    numstr += "  "
                else:
                    numstr += " "
        print(rowstr, "    ", numstr)

#Flip the coin at the nth location on board
def flip(board, n):
    j = int(n % 8)
    i = int((n - j) / 8)
    if board[i][j] == 'H':
        board[i][j] = 'T'
    else:
        board[i][j] = 'H'
    return board

#Get the nth row from board
def row(board, n):
    return board[n]

#Get the nth column from board
def col(board, n):
    return [row[n] for row in board]

#Solve board
def solve(board):
    #Split board into groups
    groups = [group(board, i) for i in range(1, 7)]
    #Convert group sums into on/off bits
    bits = [convert(g) for g in groups]
    return calculate(bits)

#Convert Heads and Tails to ones and zeroes respectively for math
def convert(lst):
    return [1 if c == 'H' else 0 for c in lst]

#Return the binary conversion of the given group sums a-f
def calculate(groups):
    #Group sums
    summed = [sum(g) for g in groups]
    #Parity bits of each group sum
    parity_bits = [s % 2 for s in summed]
    #Binary conversion helper list comprehension
    twos = [2 ** i for i in range(6)]
    return sum([parity_bits[j] * twos[j] for j in range(6)])

#Return the nth group of board
def group(board, n):
    #Odd cols
    if n == 1:
        g = []
        for i in range(8):
            if i % 2 == 1:
                g += col(board, i)
        return g
    #Cols 2, 3, 6, 7
    elif n == 2:
        g = []
        for i in range(8):
            if i % 4 == 2 or i % 4 == 3:
                g += col(board, i)
        return g
    #Right half of board
    elif n == 3:
        g = []
        for i in range(4, 8):
            g += col(board, i)
        return g
    #Odd rows
    elif n == 4:
        g = []
        for i in range(8):
            if i % 2 == 1:
                g += row(board, i)
        return g
    #Rows 2, 3, 6, 7
    elif n == 5:
        g = []
        for i in range(8):
            if i % 4 == 2 or i % 4 == 3:
                g += row(board, i)
        return g
    #Bottom half of board
    elif n == 6:
        g = []
        for i in range(4, 8):
            g += row(board, i)
        return g
    #Input error
    else:
        print("Grouping error")
        return None
