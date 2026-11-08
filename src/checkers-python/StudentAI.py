from random import randint
from BoardClasses import Move
from BoardClasses import Board

import time # TIME LIMIT FOR MCTS
import math # MATH FUNCTIONS FOR UCB1
import copy # DEEP COPY THE BOARD

#The following part should be completed by students.
#Students can modify anything except the class name and exisiting functions and varibles.

# OPPONENT LOOKUP DICTIONARY TO GET THE OPPONENT'S COLOR
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
        self._untried_moves = self._untried_moves_flattened()


    def _untried_moves_flattened(self):
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


    def best_child(self, ai_color, exploration_weight=1.4):
        '''
        Selects the best child node based on the UCB1 formula
        @param ai_color: The color of the AI player
        @param exploration_weight: The weight for exploration vs exploitation
        @return: The child node with the highest UCB1 value
        '''
        for child in self.children:
            if child.visits == 0:
                return child
            
        choices_weights = []

        for child in self.children:
            win_rate = child.wins / child.visits

            if self.color != ai_color:
                win_rate = 1 - win_rate

            choices_weights.append(win_rate + exploration_weight
                                   * math.sqrt((2 * math.log(self.visits) / child.visits)))
        
        return self.children[choices_weights.index(max(choices_weights))]


    def is_terminal_node(self):
        '''
        Checks if the current node is a terminal node
        @return: True if the game is over, False otherwise
        '''
        if self.board.is_win(OPPONENT[self.color]) != 0:
            return True
        
        return self.is_fully_expanded() and len(self.children) == 0


    def rollout_policy(self, possible_moves):
        '''
        Selects a random move from the possible moves
        @param possible_moves: The list of possible moves
        @return: A randomly selected move
        '''
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

        
    def get_move(self, move):
        if len(move) != 0:
            self.board.make_move(move,self.opponent[self.color])
        else:
            self.color = 1

        moves = self._flattened_moves(self.board.get_all_possible_moves(self.color))

        if not moves:
            return None

        # APPLY MCTS TO GET THE BEST MOVE INSTEAD OF RANDOM MOVE (IN ORIGINAL CODE, WE WERE SELECTING A RANDOM MOVE)
        root = MCTSNode(copy.deepcopy(self.board), self.color)         # CREATE A ROOT NODE FOR MCTS WITH THE CURRENT BOARD STATE AND PLAYER COLOR
        best_move = self.mcts(root, self.time_limit)    # SEACH FOR THE BEST MOVE USING MCTS WITH A TIME LIMIT

        if best_move is None:
            best_move = moves[0]    # IF MCTS FAILS TO FIND A MOVE, SELECT THE FIRST MOVE FROM THE LIST OF LEGAL MOVES
        
        self.board.make_move(best_move,self.color)
        return best_move

    
    def moves_equal(self, move1, move2):
        # FIND THE OPPONENT'S MOVE IN THE LIST OF MOVES AND RETURN TRUE IF THEY ARE EQUAL, FALSE OTHERWISE
        return str(move1) == str(move2)


    def undo_move(self):
        # UNDO THE MOVE ON THE BOARD
        self.board.undo()


    def _flattened_moves(self, moves):
        '''
        Flattens the 2D list of untried moves into a 1D list
        @return: A 1D list of untried moves
        '''
        flattened = []

        for move_list in moves:
            for move in move_list:
                flattened.append(move)

        return flattened
    
    ### MCTS STEPS ###
    
    def _selection(self, node):
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
                current_node = current_node.best_child(self.color)  # MOVE TO THE BEST CHILD NODE BASED ON UCB1
       
        return current_node  # RETURN THE LEAF NODE

    
    def _expansion(self, node):
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

    
    def _simulation(self, node):
        '''
        Simulates a random game from the current node
        @param node: The node to simulate from
        @return: The result of the simulation
        '''
        current_board = copy.deepcopy(node.board)
        current_color = node.color
        
        while current_board.is_win(OPPONENT[current_color]) == 0:
            legal_moves = self._flattened_moves(current_board.get_all_possible_moves(current_color))
            
            if not legal_moves:
                break
            
            move = node.rollout_policy(legal_moves)
            current_board.make_move(move, current_color)
            current_color = OPPONENT[current_color]
        
        result = current_board.is_win(OPPONENT[current_color])

        if result == -1:
            return 0.5
        if result == self.color:
            return 1
        else:
            return 0

    
    def _backpropagation(self, node, result):
        '''
        Backpropagates the result of the simulation up the tree
        @param node: The node to backpropagate from
        @param result: The result of the simulation
        '''
        while node is not None:
            node.visits += 1
            node.wins += result
            node = node.parent

    
    def mcts(self, root, time_limit):
        # IMPLEMENT THE MCTS ALGORITHM WITH A TIME LIMIT
        end_time = time.time() + time_limit # TIME LIMIT FOR MCTS TO STOP

        while time.time() < end_time:
            leaf_node = self._selection(root)  # SELECTION STEP
            child_node = self._expansion(leaf_node)  # EXPANSION STEP
            result = self._simulation(child_node)  # SIMULATION STEP
            self._backpropagation(child_node, result)  # BACKPROPAGATION STEP
    
        if not root.children:
            return None

        best_child = max(root.children, key=lambda c: c.visits)  # SELECT THE CHILD WITH THE MOST VISITS
        return best_child.parent_move  # RETURN THE MOVE THAT LED TO THE BEST CHILD
    