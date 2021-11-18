import random

all_dominoes = [[2, 5], [1, 2], [3, 6], [0, 0], [0, 2], [5, 6], [
    3, 5], [2, 4], [3, 4], [1, 5], [0, 4], [2, 6], [3, 3], [1, 1], [1, 4], [1, 3], [2, 3], [4, 5], [2, 2], [0, 3], [0, 6], [5, 5], [4, 4], [4, 6], [0, 1], [0, 5], [1, 6], [6, 6]]

# Number of dominoes = 28.
# 7 dominoes in 1st set starting with 0.  6 in second set starting with 1 (0x6 already accounted for).  5 in 3rd set starting with 2 etc.
# Therefore number of dominoes = 7+6+5+4+3+2+1 = 28
# Also this formula: (n+1)(n+2)/2 or (n^2+3n+2)/2 where n is the largest domino so can be used for larger sets.

stock_pieces = all_dominoes[:]


computer_pieces = random.sample(stock_pieces, 7)
stock_pieces = [tile for tile in stock_pieces if tile not in computer_pieces]

player_pieces = random.sample(stock_pieces, 7)
stock_pieces = [tile for tile in stock_pieces if tile not in player_pieces]


domino_snake = []
winner = ""
status = "stock"

while status == "stock":
    double = 6
    while double >= 0:
        if [double, double] in stock_pieces:
            double -= 1
        elif [double, double] in computer_pieces:
            status = "player"
            domino_snake.append([double, double])
            computer_pieces.remove([double, double])
            break
        elif [double, double] in player_pieces:
            status = "computer"
            domino_snake.append([double, double])
            player_pieces.remove([double, double])
            break


def print_snake():
    if len(domino_snake) < 6:
        print(*domino_snake)
    else:
        print(*domino_snake[0:3],"...",*domino_snake[-3:])


def endgame():
    global gameon
    if domino_snake[0][0] == domino_snake[-1][0] and sum(x.count(domino_snake[0][0]) for x in domino_snake) == 8:
        gameon = 0
        print()
        print("Status: The game is over. It's a draw!")
    elif domino_snake[0][1] == domino_snake[-1][1] and sum(x.count(domino_snake[0][1]) for x in domino_snake) == 8:
        gameon = 0
        print()
        print("Status: The game is over. It's a draw!")
    elif len(stock_pieces) == 0:
        gameon = 0
        print()
        print("Status: The game is over. It's a draw!")
    elif len(computer_pieces) == 0:
        gameon = 0
        print()
        print("Status: The game is over. The computer won!")
    elif len(player_pieces) == 0:
        gameon = 0
        print()
        print("Status: The game is over. You won!")


def game_move(userinput):
    global player_pieces, computer_pieces, domino_snake
    left_tile = domino_snake[0][0]
    right_tile = domino_snake[-1][1]
    # print(left_tile, right_tile, userinput)
    if status == "player":
        if abs(userinput) not in range(0, len(player_pieces)+1):
            userinput = int(input(("Invalid input. Please try again.\n")))
            game_move(userinput)
        elif userinput < 0 and left_tile not in player_pieces[-userinput-1]:
            # print(left_tile, player_pieces[-userinput-1])
            userinput = int(input(("Illegal move. Please try again.\n")))
            game_move(userinput)
        elif userinput > 0 and right_tile not in player_pieces[userinput-1]:
            # print(right_tile, player_pieces[userinput-1])
            userinput = int(input(("Illegal move. Please try again.\n")))
            game_move(userinput)
        else:
            player_move(userinput)

    if status == "computer":
        if userinput != "":
            userinput = ("Invalid input. Please try again.\n")
            game_move(userinput)
        else:
            comp_move()


def player_move(userinput):
    global player_pieces, computer_pieces, domino_snake
    left_tile = domino_snake[0][0]
    right_tile = domino_snake[-1][1]
    if userinput < 0:
        move = player_pieces.pop(-userinput-1)
        # print(move, move[::-1], left_tile)
        domino_snake.insert(0, move) if move[1] == left_tile else domino_snake.insert(0, move[::-1])
        # domino_snake.insert(0, move)
    elif userinput > 0:
        move = player_pieces.pop(userinput-1)
        # print(move, move[::-1], right_tile)
        domino_snake.append(move) if move[0] == right_tile else domino_snake.append(move[::-1])
        # domino_snake.append(move)
    elif userinput == 0:
        new_tileidx = stock_pieces.index(random.sample(stock_pieces, 1)[0])
        new_tile = stock_pieces.pop(new_tileidx)
        player_pieces.append(new_tile)

def comp_move():
    global player_pieces, computer_pieces, domino_snake
    
    # dictionary for count of nums across computer pieces and snake
    count = dict({0: 0, 1: 0, 2: 0, 3: 0, 4: 0, 5: 0, 6: 0})
    for i in range(7):
        points_count = sum(x.count(i) for x in domino_snake) + sum(x.count(i) for x in computer_pieces)
        count[i] = points_count

    # counts scores for each of the computer's pieces to determine which should be played first
    points_total = [count.get(computer_pieces[i][0]) + count.get(computer_pieces[i][1]) for i in range(len(computer_pieces))]
    # max_points_idx = points_total.index(max(points_total))

    left_tile = domino_snake[0][0]
    right_tile = domino_snake[-1][1]
    available_tiles = []
    available_tiles = [tile for tile in computer_pieces if left_tile in tile or right_tile in tile]

    #  check if there are dominoes that can be played and make the move
    while True:
        max_points_idx = points_total.index(max(points_total))

        if len(available_tiles) == 0 and stock_pieces:
            new_tileidx = stock_pieces.index(random.sample(stock_pieces, 1)[0])
            new_tile = stock_pieces.pop(new_tileidx)
            computer_pieces.append(new_tile)
            break

        elif left_tile in computer_pieces[max_points_idx]:
            tile = computer_pieces.index(available_tiles[0])
            move = computer_pieces.pop(tile)
            domino_snake.insert(0, move) if move[1] == left_tile else domino_snake.insert(0, move[::-1])
            break
            
        elif right_tile in computer_pieces[max_points_idx]:
            tile = computer_pieces.index(available_tiles[0])
            move = computer_pieces.pop(tile)
            domino_snake.append(move) if move[0] == right_tile else domino_snake.append(move[::-1])
            break

        else:
            points_total[max_points_idx] = -1
            continue
       
def change_player():
    global status
    if status == "player":
        status = "computer"
    else:
        status = "player"


gameon = 1
while gameon == 1:
    print("=" * 70)
    print("Stock size:", len(stock_pieces))
    print("Computer pieces:", len(computer_pieces))
    print()
    print_snake()
    print()

    print("Your pieces:")
    for count, tile in enumerate(player_pieces, 1):
        print(f"{count}:{tile}")

    endgame()  # checks status of game before continuing need a break for the loop if winner exists
    if gameon == 0:
        break
        
    userinput = False
    if status == "player":
        print()
        while type(userinput) is not int:
            try:
                userinput = int(input(
                    "Status: It's your turn to make a move.  Enter your command. \n"))
                game_move(userinput)
            except ValueError:
                userinput = int(input("Invalid input. Please try again.\n"))
    elif status == "computer":
        print()
        userinput = input(
            "Status: Computer is about to make a move.  Press Enter to continue...\n")
        game_move(userinput)
    
    change_player()