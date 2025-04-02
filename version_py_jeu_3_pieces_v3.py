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

    # Parcours des coups possibles sur les cellules vides, en excluant move_to_change s'il est défini.
    for cell in empty_cells(state):
        if move_to_change is not None and cell == move_to_change:
            continue
        x, y = cell[0], cell[1]
        state[x][y] = player
        score = minimax(state, depth - 1, -player, move_to_change)
        state[x][y] = 0
        # On attribue ici le mouvement testé (la position où on a joué)
        score[0], score[1] = x, y
        
        if player == COMP:
            if score[2] > best[2]:
                best = score  # on maximise
        else:
            if score[2] < best[2]:
                best = score  # on minimise
    
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
        return None
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

def human_turn(c_choice, h_choice):
    """
    The Human plays choosing a valid move.
    :param c_choice: computer's choice X or O
    :param h_choice: human's choice X or O
    :return:
    """
    moves = {
        1: [0, 0], 2: [0, 1], 3: [0, 2],
        4: [1, 0], 5: [1, 1], 6: [1, 2],
        7: [2, 0], 8: [2, 1], 9: [2, 2],
    }
    print(f"\nHuman turn [{h_choice}]")
    render(board, c_choice, h_choice)
    
    # Si l'humain possède déjà 3 pièces, il doit déplacer la plus ancienne.
    if len(human_history) == 3:
        old_piece = human_history.pop(0)
        board[old_piece[0]][old_piece[1]] = 0
        print(f"Vous devez déplacer votre plus ancienne pièce, située en {old_piece}.")
    
    # Demande le nouveau coup à jouer.
    while True:
        try:
            move_input = input("Entrez votre coup (1-9): ")
            h_move = int(move_input)
            if h_move not in moves:
                print("Coup invalide. Veuillez entrer un nombre entre 1 et 9.")
                continue
            coord = moves[h_move]
            if not valid_move(coord[0], coord[1]):
                print("Coup invalide, case déjà occupée. Réessayez.")
                continue
            # Pose le coup et enregistre-le dans l'historique.
            set_move(coord[0], coord[1], HUMAN)
            human_history.append(coord)
            break
        except ValueError:
            print("Entrée invalide. Veuillez entrer un nombre.")
    print("Coup validé.\n")

################# POINT D'ENTRÉE DU PROGRAMME #################

if __name__ == '__main__':
    # Initialisation pour le mode terminal (partie de morpion à 3 pièces)
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
    
    # Choix des symboles
    h_choice = 'v'  # symbole de l'humain
    c_choice = '*'  # symbole de l'IA
    
    print("Bienvenue dans le Morpion à 3 pièces !")
    first_choice = input("Qui commence ? (H pour l'humain, sinon l'IA commencera) : ")
    # On définit le joueur courant : si 'H' est saisi, c'est l'humain qui débute, sinon l'IA
    if first_choice.upper() == 'H':
        current_player = HUMAN
    else:
        current_player = COMP
    
    # Boucle principale du jeu
    while len(empty_cells(board)) > 0 and not game_over(board):
        if current_player == HUMAN:
            human_turn(c_choice, h_choice)
            current_player = COMP
        else:
            ai_move = ai_turn(c_choice, h_choice)
            print(f"L'IA a joué: {ai_move}")
            current_player = HUMAN
    
    # Affichage final et annonce du résultat
    render(board, c_choice, h_choice)
    if wins(board, HUMAN):
        print("\nL'humain gagne !")
    elif wins(board, COMP):
        print("\nL'IA gagne !")
    else:
        print("\nMatch nul !")
