#!/usr/bin/python
# credits: http://www.binarytides.com/python-socket-server-code-example/

'''
	Simple socket server using threads
'''

import socket
import sys
from math import inf as infinity
from random import choice
import platform
import time
from os import system
import numpy as np
import copy  # Si besoin pour des copies profondes 

# Déclarations globales
# Les joueurs sont représentés par des entiers:
# HUMAN = -1 (joueur humain) et COMP = +1 (ordinateur)
HUMAN = -1
COMP = +1
board = None  # Le plateau sera initialisé plus bas

# Listes pour suivre l'ordre des coups de chaque joueur
human_history = []
comp_history = []


################# FUNCTIONS ################
def evaluate(state):
    """
    Function to heuristic evaluation of state.
    :param state: the state of the current board
    :return: +1 if the computer wins; -1 if the human wins; 0 draw
    """
    if wins(state, COMP):
        score = +1
    elif wins(state, HUMAN):
        score = -1
    else:
        score = 0

    return score


def wins(state, player):
    """
    This function tests if a specific player wins. Possibilities:
    * Three rows    [X X X] or [O O O]
    * Three cols    [X X X] or [O O O]
    * Two diagonals [X X X] or [O O O]
    :param state: the state of the current board
    :param player: a human or a computer
    :return: True if the player wins
    """
    win_state = [
        [state[0][0], state[0][1], state[0][2]],
        [state[1][0], state[1][1], state[1][2]],
        [state[2][0], state[2][1], state[2][2]],
        [state[0][0], state[1][0], state[2][0]],
        [state[0][1], state[1][1], state[2][1]],
        [state[0][2], state[1][2], state[2][2]],
        [state[0][0], state[1][1], state[2][2]],
        [state[2][0], state[1][1], state[0][2]],
    ]
    if [player, player, player] in win_state:
        return True
    else:
        return False


def game_over(state):
    """
    This function test if the human or computer wins
    :param state: the state of the current board
    :return: True if the human or computer wins
    """
    return wins(state, HUMAN) or wins(state, COMP)


def empty_cells(state):
    """
    Each empty cell will be added into cells' list
    :param state: the state of the current board
    :return: a list of empty cells
    """
    cells = []

    for x, row in enumerate(state):
        for y, cell in enumerate(row):
            if cell == 0:
                cells.append([x, y])

    return cells


def valid_move(x, y):
    """
    A move is valid if the chosen cell is empty
    :param x: X coordinate
    :param y: Y coordinate
    :return: True if the board[x][y] is empty
    """
    if [x, y] in empty_cells(board):
        return True
    else:
        return False


def set_move(x, y, player):
    """
    Set the move on board, if the coordinates are valid
    :param x: X coordinate
    :param y: Y coordinate
    :param player: the current player
    """
    if valid_move(x, y):
        board[x][y] = player
        return True
    else:
        return False


def minimax(state, depth, player, move_to_change=None):
    """
    AI function that choice the best move
    :param state: current state of the board
    :param depth: node index in the tree (0 <= depth <= 9),
    but never nine in this case (see iaturn() function)
    :param player: an human or a computer
    :param move_to_change: (optionnel) un tuple (i,j) indiquant la case à exclus des mouvements possibles.
    :return: a list with [the best row, best col, best score]
    """
    if player == COMP:
        best = [-1, -1, -infinity]
    else:
        best = [-1, -1, +infinity]

    if depth == 0 or game_over(state):
        score = evaluate(state)
        return [-1, -1, score]

    for cell in empty_cells(state):
        if move_to_change is not None and cell == move_to_change:
            continue
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player, move_to_change)
        state[x][y] = 0
        score[0], score[1] = x, y

        if player == COMP:
            if score[2] > best[2]:
                best = score  # max value
        else:
            if score[2] < best[2]:
                best = score  # min value

    return best


def clean():
    """
    Clears the console
    """
    os_name = platform.system().lower()
    if 'windows' in os_name:
        system('cls')
    else:
        system('clear')


def render(state, c_choice, h_choice):
    """
    Print the board on console
    :param state: current state of the board
    """

    chars = {
        -1: h_choice,
        +1: c_choice,
        0: ' '
    }
    str_line = '---------------'

    print('\n' + str_line)
    for row in state:
        for cell in row:
            symbol = chars[cell]
            print(f'| {symbol} |', end='')
        print('\n' + str_line)


def ai_turn(c_choice, h_choice):
    moves = {
        "00" :1 , "01" :2 , "02" :3 ,
        "10" :4 , "11" :5 , "12" :6 ,
        "20" :7 , "21" :8 , "22" :9 ,
    }
    """
    It calls the minimax function if the depth < 9,
    else it choices a random coordinate.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    #clean()
    print(f'Computer turn [{c_choice}]')
    render(board, c_choice, h_choice)
    
    # Si l'IA a déjà 3 pièces, déplacer la pièce la plus ancienne.
    popped_cell = None
    if len(comp_history) == 3:
        popped_cell = comp_history.pop(0)
        board[popped_cell[0]][popped_cell[1]] = 0
        print(f"L'IA déplace sa plus ancienne pièce, située en {popped_cell}.")
    
    # Appel de minimax en passant popped_cell comme coup à exclure.
    move = minimax(board, depth, COMP, popped_cell)
    x, y = move[0], move[1]


    # On joue le coup trouvé et on met à jour l'historique.
    set_move(x, y, COMP)
    comp_history.append([x, y])
    time.sleep(1)
    return moves[str(x)+str(y)]


def data_to_mat(data):
    #data a cette forme [[0,0,0,0,0],[0,0,0,0,0]]
    moves = {
            1: [0, 0], 2: [0, 1], 3: [0, 2],
            4: [1, 0], 5: [1, 1], 6: [1, 2],
            7: [2, 0], 8: [2, 1], 9: [2, 2],
        }
        
    data = data.replace('[','')
    data = data.replace(']','')
    values = data.split(',')
    noir = []
    for i in range(0,5):
        noir.append(int(values[i]))
    blanc = []
    for i in range(5,10):
        blanc.append(int(values[i]))
        
    print("noir")
    print(noir)

    print("blanc")
    print(blanc)

    received_board = [
    [0, 0, 0],
    [0, 0, 0],
    [0, 0, 0],
    ]
    for n in noir:
        if n != 0:
            coord = moves[n]
            received_board[coord[0]][coord[1]] = HUMAN

    for b in blanc:
        if b != 0:
            print("b= ",b)
            coord = moves[b]
            print("coord",coord)
            received_board[coord[0]][coord[1]] = COMP
    
    return received_board

    
def is_new(n_board):
    if np.array_equal(n_board, board):
        print("is_new false")
        return False
    else:
        print("is_new true")
        return True


def un_coup(n_board):
    coup = 0
    for i in range (0,3):
        for j in range (0,3):
            if n_board[i][j] == -1 and board[i][j] == 0:
                coup = coup + 1
    if coup > 1 :
        print("plus q'un coup joué")
        return False
    return True


def is_correct(n_board):
    for i in range (0,3):
        for j in range (0,3):
            if board[i][j] != n_board[i][j]: 
                print(board[i][j], "different",n_board[i][j])
                if n_board[i][j] != -1 :
                    print("n_board[i][j] != -1 is_correct false")
                    return False
                else:
                    if board[i][j] != 0:
                        print("board[i][j] != 0 is_correct false")
                        return False
    print("is_correct True")
    return True

def bad_value(data):
    if "-1"  in data:
        print("-1 in data")
        return True
    return False
        
def data2move(data):
    if bad_value(data) == False:
        n_board = data_to_mat(data)
        print("board")
        print(board)
        print("new_board")
        print(n_board)
        moves = {
            "00" :1 , "01" :2 , "02" :3 ,
            "10" :4 , "11" :5 , "12" :6 ,
            "20" :7 , "21" :8 , "22" :9 ,
        }
        if is_new(n_board) == True and is_correct(n_board) == True and un_coup(n_board)==True:
            diff = np.asarray(n_board) - np.asarray(board)
            for i in range(0,3):
                for j in range(0,3):
                    if diff[i][j]==-1:
                        print("-1 is at ",i,j)
                        return moves[str(i)+str(j)]
        else:
            print("else")
    return -1
                    
            
        
        
def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    depth = len(empty_cells(board))
    if depth == 0 or game_over(board):
        return

    # Dictionary of valid moves
    h_move = -1
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }

    #clean()
    print(f'Human turn [{h_choice}]')
    render(board, c_choice, h_choice)

    # Si l'humain possède déjà 3 pièces, il doit déplacer la plus ancienne.
    if len(human_history) == 3:
        old_piece = human_history.pop(0)
        board[old_piece[0]][old_piece[1]] = 0
        print(f"Vous devez déplacer votre plus ancienne pièce, située en {old_piece}.")
        send("MOVE_OLD")  

    # lire le coup de l'humain
    while h_move == -1:
        try:
            
            print("\ndonner le coup du joueur")
            data = receive() #[[0,0,0,0,0],[0,0,0,0,0]]
            h_move = data2move(data)
            if h_move == -1:
                print('\nBad move 1')
                render(board, c_choice, h_choice)
                send("-1")
            else:    
                coord = moves[h_move]
                can_move = set_move(coord[0], coord[1], HUMAN)

                if not can_move:                   
                    h_move = -1
                    print('\nBad move 2')
                    render(board, c_choice, h_choice)
                    send("-1")
                    
        except (EOFError, KeyboardInterrupt):
            print('\nBye')
            exit()
        except (KeyError, ValueError):
            print('\nBad choice')
    
    print("\ncoup joueur fini")
    
    
def send(msg):
    try :
        conn.sendall(msg.encode('utf-8'))
    except socket.error:
        #Send failed
        print ('Send failed')
        #return -1#sys.exit()

def receive():
    data = conn.recv(1024)
    d = data.decode('UTF-8')  
    d = d.rstrip()
    return d
        
HOST = ''	# Symbolic name, meaning all available interfaces
PORT = 21	# Arbitrary non-privileged port

s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
print ('Socket created')

#Bind socket to local host and port
try:
	s.bind((HOST, PORT))
except socket.error as msg:
	print ('Bind failed. Error Code : ' + str(msg[0]) + ' Message ' + msg[1])
	sys.exit()
	
print ('Socket bind complete')

#Start listening on socket
s.listen(1)
print ('Socket now listening')
print ('Click on START in RobotStudio')

#now keep talking with the client

#wait to accept a connection - blocking call
conn, addr = s.accept()

print ('Connected with ' + addr[0] + ':' + str(addr[1]))
print ('Check with YUMI to start the GAME')

try:
    while 1:
        data = receive()
        print("data=",data)

        while data != 'D':
            send("requete {} est inavalide".format(data))
            data = receive()

        send("TRUE") 

        print ("début de la partie")
        # initialisation

        HUMAN = -1
        COMP = +1
        board = [
            [0, 0, 0],
            [0, 0, 0],
            [0, 0, 0],
        ]
        # Réinitialisation des historiques
        human_history = []
        comp_history = []

        h_choice = 'v'
        c_choice = '*'
        first = ''

        print("choix du 1er joueur")

        #send("Qui va jouer le premier?") 
        #data = receive()  
        #while data != 'H' and data != 'R':
        #    send("requete inavalide, entrer à nouveau")
        #    data = receive()
        data = "H"    
        if data == "H":    
            first = 'Y'
        else:
            first = 'N'
            
        # Main loop of this game
        while len(empty_cells(board)) > 0 and not game_over(board):
            if first == 'N':
                ai_move = ai_turn(c_choice, h_choice)
                first = ''
                print("voici le coup à jouer",ai_move)
                send(str(ai_move))
            
            
            human_turn(c_choice, h_choice)
            ai_move = ai_turn(c_choice, h_choice)
            print("voici le coup à jouer")
            send(str(ai_move))

        if wins(board, HUMAN) == False and wins(board, COMP) == False:
            send(str(ai_move))
            
        data = receive()
            
        # Game over message
        if wins(board, HUMAN):
            #clean()
            print(f'Human turn [{h_choice}]')
            render(board, c_choice, h_choice)
            print('Human is the winner!')
            send('-300')
            print('send finished')

        elif wins(board, COMP):
            #clean()
            print(f'Computer turn [{c_choice}]')
            render(board, c_choice, h_choice)
            print('YUMI is the winner!')
            send('-200')
            print('send finished')
        else:
            #clean()
            render(board, c_choice, h_choice)
            print('DRAW')
            #send(str(ai_move))
            #time.sleep(10)
            send('-400')
            print('send finished')
except KeyboardInterrupt:
    print("Goodbye!")
    s.close()
    pass
