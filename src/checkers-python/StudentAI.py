from random import randint
from BoardClasses import Move
from BoardClasses import Board

import time # TIME LIMIT FOR MCTS
import math # MATH FUNCTIONS FOR UCB1

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

class MCTSNode:
    def __init__(self, board, color, move=None, parent=None):
        self.board = board
        self.color = color
        self.move = move  # the move that got us to this node - "None" for the root node
        self.parent = parent
        self.children = []
        self.visits = 0
        self.wins = 0
        self._untried_moves = self._untried_moves_flattened()

    def _untried_moves_flattened(self):
        moves = self.board.get_all_possible_moves(self.color)
        flattened = []
        for move_list in moves:
            for move in move_list:
                flattened.append(move)
        return flattened

    def is_fully_expanded(self):
        pass

    def best_child(self, exploration_weight):
        pass

    def most_visited_child(self):
        pass

class StudentAI():

    def __init__(self,col,row,p):
        self.col = col
        self.row = row
        self.p = p
        self.board = Board(col,row,p)
        self.board.initialize_game()
        self.color = ''
        self.opponent = {1:2,2:1}
        self.color = 2
        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1
        moves = self.board.get_all_possible_moves(self.color)
        index = randint(0,len(moves)-1)
        inner_index =  randint(0,len(moves[index])-1)
        move = moves[index][inner_index]
        self.board.make_move(move,self.color)
        return move
    
    def moves_equal(self, move1, move2):
        # FIND THE OPPONENT'S MOVE IN THE LIST OF MOVES AND RETURN TRUE IF THEY ARE EQUAL, FALSE OTHERWISE
        pass
    
    def undo_move(self, move):
        # UNDO THE MOVE ON THE BOARD
        pass
    
    ### MCTS STEPS ###
    
    def selection(self, node):
        # SELECT THE BEST CHILD NODE BASED ON UCB1 FORMULA
        pass
    
    def expansion(self, node):
        # EXPAND THE NODE BY ADDING A NEW CHILD NODE FOR AN UNTRIED MOVE
        pass
    
    def simulation(self, node):
        # SIMULATE A RANDOM GAME FROM THE CURRENT NODE AND RETURN THE RESULT
        pass
    
    def backpropagation(self, node, result):
        # BACKPROPAGATE THE RESULT OF THE SIMULATION UP THE TREE
        pass
    
    def mcts(self, root, time_limit):
        # IMPLEMENT THE MCTS ALGORITHM WITH A TIME LIMIT
        pass
    
    