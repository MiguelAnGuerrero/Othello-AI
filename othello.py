from OthelloEngine import get_all_moves
import random
from copy import deepcopy, copy
from threading import Thread

class Othello_AI:
    def __init__(self, team_type, board_size=8, time_limit=2.0):
      # team_type will be either 'W' or 'B', indicating what color you are
      # board_size and time_limit will likely stay constant, but if you want this can add different challanges
        self.team_type = team_type
      
      
    def get_move(self, board_state):
      # board state will be an board_size by board_size array with the current state of the game.
      #       Possible values are: 'W', 'B', or '-'
      # Return your desired move (If invalid, instant loss)
      # Example move: ('W', (1, 6))
        ai_state = deepcopy(board_state)
        result =[0] * 6
        threads =[0] * 6
        for i in len(threads):
            threads[i] = Thread(target=monte_carlo_tree_search, args=(ai_state, result, i, 1000))
        
        max_state = max(result, key=lambda p: p.N)
        move = result.get(max_state).move
        #moves = get_all_moves(board_state, self.team_type)
        #if len(moves) > 0:
         #   return random.choice(moves)
        for i in len(threads):
            threads[i].join()
     
        return move
      
    def get_team_name(self):
      # returns a string containing your team name
      return "Dylan and Miguel"

#SECOND SECTION

def piece_count(test_state, team):
        black_pieces = 0
        white_piece = 0
        for i in test_state:
            for j in test_state[i]:
                if j == 'B':
                    black_pieces +=1
                if j == 'W':
                    white_piece += 1
        if team == 'B':
            return black_pieces - white_piece
        else:
            return white_piece - black_pieces
        
def move_count(test_state, team):
    w_moves = get_all_moves(test_state, 'W')
    b_moves = get_all_moves(test_state, 'B')
    if team == 'W':
        return len(w_moves) - len(b_moves)
    else:
        return len(b_moves) - len(w_moves)


class MCT_Node:
    """Node in the Monte Carlo search tree, keeps track of the children states."""

    def __init__(self, parent=None, state=None, team=None, move=None, U=0, N=0):
        self.__dict__.update(parent=parent, state=state, team=team, move=move, U=U, N=N)
        self.children = {}
        self.actions = None


def ucb(n, C=1.4):
    return inf if n.N == 0 else n.U / n.N + C * math.sqrt(math.log(n.parent.N) / n.N)



#This implementation is based off of the one in the games4e section of the github we have been using all year.
def monte_carlo_tree_search(state, result, resultNumber, N=1000):
    
    def utility(test_state, player):
        result += piece_count(test_state, player)
        result += move_count(test_state, player)
        return result
    
    def select(n):
        """select a leaf node in the tree"""
        if n.children:
            return select(max(n.children.keys(), key=ucb))
        else:
            return n
        
        
    #Rewrite this instead of game functions such as result and action, write own methods to replace them.    
    def terminal_test(state):
        moves = get_all_moves(state)
        if len(moves) == 0:
            return True
        
    def reverse(team):
        if team == 'B':
            return 'W'
        else: 
            return 'B'

    """expand the leaf node by adding all its children states"""
    def expand(n):
        if not n.children and not terminal_test(n.state):
            n.children = {MCT_Node(state=update_board(n.state, action),team = reverse(n.team), move=action, parent=n): action
                      for action in get_all_moves(n.state, n.team)}
        return select(n)
    
    
    
    def simulate(test_state, team):
        """simulate the utility of current state by random picking a step"""
        player = team
        while not terminal_test(test_state):
            action = random.choice(list(get_all_moves(test_state, team)))
            test_state = update_board(test_state, action)
        v = utility(test_state, player)
        return -v
    
    
    
    def backprop(n, utility):
        """passing the utility back to all parent nodes"""
        if utility > 0:
            n.U += utility
        # if utility == 0:
        #     n.U += 0.5
        n.N += 1
        if n.parent:
            backprop(n.parent, -utility)    
            
            
        
    root = MCT_Node(state=state, team = team)

    for _ in range(N):
        leaf = select(root)
        child = expand(leaf)
        result = simulate(child.state, child.team)
        backprop(child, result)

    max_state = max(root.children, key=lambda p: p.N)
    #return entire child. Probably just return action that created it.
    result[resultNumber] = root.children.get(max_state)



#///////////////////////////////////////////////////////////

def update_board(state, move):
      # move format: ('B', (i, j)) or ('B', None)
      # update the board state given the current move
      # if the move is None, do nothing
      # Assume that is a valid move, no need for extra error checking
        newState = deepcopy(state)
        if move[1] is not None:
            r = move[1][0]
            c = move[1][1]
            color = move[0]

         #left
            i = r
            j = c - 1
            while j >= 0:
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    j -= 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at c-1
                        for index in range(c - j - 1):
                            newState[i][j + index + 1] = color
                #end the loop
                    break

         #left-up direction
            i = r - 1
            j = c - 1
            while i >= 0 and j >= 0:
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i -= 1
                    j -= 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at c-1, r-1
                        for index in range(c - j - 1):
                            newState[i + index + 1][j + index + 1] = color
                #end the loop
                    break

         #up
            i = r -1
            j = c
            while i >= 0:
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i -= 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at r-1
                        for index in range(r - i - 1):
                            newState[i + index + 1][j] = color
                #end the loop
                    break

         #right-up direction
            i = r - 1
            j = c + 1
            while i >= 0 and j < len(newState):
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i -= 1
                    j += 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at r-1, c+1
                        for index in range(r - i - 1):
                            newState[i + index + 1][j - index - 1] = color
                #end loop
                    break

         #right direction
            i = r
            j = c + 1
            while j < len(state):
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    j += 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at c+1
                        for index in range(j - c - 1):
                            newState[i][j - index - 1] = color
                #end loop
                    break

         #right-down
            i = r + 1
            j = c + 1
            while i < len(newState) and j < len(newState):
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i += 1
                    j += 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at r+1,c+1
                        for index in range(j - c - 1):
                            newState[i - index - 1][j - index - 1] = color
                #end loop
                    break

         #down
            i = r + 1
            j = c
            while i < len(newState):
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i += 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at r+1
                        for index in range(i - r - 1):
                            newState[i - index - 1][j] = color
                #end loop
                    break

         #left-down
            i = r + 1
            j = c - 1
            while i < len(newState) and j >= 0:
                if newState[i][j] != color and newState[i][j] != '-':
                #it's opposite color, keep checking
                    i += 1
                    j -= 1
                else:
                    if newState[i][j] == color:
                    #it's the same color, go back and change till we are at r+1
                        for index in range(i - r - 1):
                            newState[i - index - 1][j + index + 1] = color
                #end loop
                    break

         #set the spot in the game_state
            newState[r][c] = color
        return newState
