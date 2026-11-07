from random import randint
from BoardClasses import Move
from BoardClasses import Board

import time # TIME LIMIT FOR MCTS
import math # MATH FUNCTIONS FOR UCB1
import copy

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

# OPPONENT LOOKUP DICTIONARY TO GET THE OPPONENT'S COLOR
## OPPONENT[1] -> 2
## OPPONENT[2] -> 1
OPPONENT = {1:2, 2:1}

class MCTSNode:
    def __init__(self, board, color, parent=None, parent_move=None):
        self.board = board
        self.color = color
        self.parent = parent
        self.parent_move = parent_move 
        self.children = []
        self.visits = 0
        self.wins = 0
        self._untried_moves = self.untried_moves_flattened()

    def untried_moves_flattened(self):
        '''
        Flattens the 2D list of untried moves into a 1D list
        @return: A 1D list of untried moves
        '''
        moves = self.board.get_all_possible_moves(self.color)
        flattened = []
        for move_list in moves:
            for move in move_list:
                flattened.append(move)
        return flattened

    def is_fully_expanded(self):
        '''
        Checks if there's any untried moves left for this node
        @return: True if there are no untried moves left, False otherwise
        '''
        return len(self._untried_moves) == 0

    def expand(self):
        '''
        Expands the node by creating a new child node for an untried move
        @return: The newly created child node
        '''
        move = self._untried_moves.pop()
        new_board = copy.deepcopy(self.board)
        new_board.make_move(move, self.color)
        child_node = MCTSNode(new_board, OPPONENT[self.color], parent=self, parent_move=move)  
        self.children.append(child_node)
        return child_node

    def best_child(self, exploration_weight=1.0):
        '''
        Selects the best child node based on the UCB1 formula
        @param exploration_weight: The weight for exploration vs exploitation
        @return: The child node with the highest UCB1 value
        '''
        for child in self.children:
            if child.visits == 0:
                return child
        choices_weights = [(child.wins / child.visits) + exploration_weight 
                           * math.sqrt((2 * math.log(self.visits) / child.visits)) 
                           for child in self.children]
        return self.children[choices_weights.index(max(choices_weights))]

    def is_terminal_node(self):
        '''
        CHECK IF THE CURRENT NODE IS A TERMINAL NODE (I.E., THE GAME IS OVER)
        RETURN TRUE IF THE GAME IS OVER
        '''
        if self.board.is_win(OPPONENT[self.color]) != 0:
            return True
        return self.is_fully_expanded() and len(self.children) == 0

    def rollout_policy(self, possible_moves):
        # SELECT A RANDOM MOVE FROM THE POSSIBLE MOVES
        return possible_moves[randint(0, len(possible_moves) - 1)]
        
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
        self.time_limit = 1.0  # SET A TIME LIMIT FOR THINKING (IN SECONDS) FOR MCTS
        
    def get_move(self,move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self.board.get_all_possible_moves(self.color)

        # APPLY MCTS TO GET THE BEST MOVE INSTEAD OF RANDOM MOVE (IN ORIGINAL CODE, WE WERE SELECTING A RANDOM MOVE)
        root = MCTSNode(self.board, self.color)         # CREATE A ROOT NODE FOR MCTS WITH THE CURRENT BOARD STATE AND PLAYER COLOR
        best_move = self.mcts(root, self.time_limit)    # SEACH FOR THE BEST MOVE USING MCTS WITH A TIME LIMIT

        self.board.make_move(best_move,self.color)
        return best_move
    
    def moves_equal(self, move1, move2):
        # FIND THE OPPONENT'S MOVE IN THE LIST OF MOVES AND RETURN TRUE IF THEY ARE EQUAL, FALSE OTHERWISE
        return str(move1) == str(move2)

    def undo_move(self, move):
        # UNDO THE MOVE ON THE BOARD
        self.board.undo()
    
    ### MCTS STEPS ###
    
    def selection(self, node):
        # SELECT THE BEST CHILD NODE BASED ON UCB1 FORMULA
        '''
        LOGIC:
        1. START FROM THE ROOT NODE
        2. LOOK AT ALL THE CHILDREN OF THE CURRENT NODE
        3. APPLY THE UCB1 FORMULA TO SELECT THE BEST CHILD NODE
        4. PICK THE CHILD WITH THE HIGHEST UCB1 VALUE AND MOVE TO THAT CHILD NODE
        5. REPEAT UNTIL A LEAF NODE IS REACHED (A NODE THAT HAS UNTRIED MOVES OR IS A TERMINAL NODE)
        6. RETURN THAT LEAF NODE
        '''
        current_node = node
        while not current_node.is_terminal_node():
            if not current_node.is_fully_expanded():
                return current_node  # RETURN THE LEAF NODE IF IT HAS UNTRIED MOVES
            else:
                current_node = current_node.best_child()  # MOVE TO THE BEST CHILD NODE BASED ON UCB1
        return current_node  # RETURN THE LEAF NODE
    
    def expansion(self, node):
        # EXPAND THE NODE BY ADDING A NEW CHILD NODE FOR AN UNTRIED MOVE
        '''
        LOGIC:
        1. IDENTIFY A LEAF NODE (THERE ARE LEGAL MOVES FROM THIS NODE THAT HAVE NOT BEEN TRIED YET)
        2. SELECT ONE OF THE UNTRIED MOVES
        3. PLAY THAT MOVE ON THE BOARD
        4. CREATE A NEW CHILD NODE WITH THE NEW BOARD STATE AND ADD IT TO THE CHILDREN OF THE CURRENT NODE
        5. RETURN THE NEW CHILD NODE
        '''
        if node.is_fully_expanded():
            return node
        child_node = node.expand()  # EXPAND THE NODE AND GET THE NEW CHILD NODE
        return child_node  # RETURN THE NEW CHILD NODE
    
    def simulation(self, node):
        # SIMULATE A RANDOM GAME FROM THE CURRENT NODE AND RETURN THE RESULT
        pass
    
    def backpropagation(self, node, result):
        # BACKPROPAGATE THE RESULT OF THE SIMULATION UP THE TREE
        pass
    
    def mcts(self, root, time_limit):
        # IMPLEMENT THE MCTS ALGORITHM WITH A TIME LIMIT
        pass
    
    