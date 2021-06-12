import queue
from itertools import count

# Used to add unique second key in queue
# So priority is first compared, then the counter
unique = count()
    
class Dijkstra:
    # Create the dijkstra with a given number of cell
    def __init__(self, k):
        self.nb_cell = k

        
        
    # Update the top node of the dijkstra, with the best known node
    def _update_top(self):
        top = self.neighborQueue.get()
        self.top_cost = top[0]
        self.top_data = top[2]
    
    
    
    # Init the queue with the first neighbors
    def _first_step(self, start, neighbors_function, cost_function):
        for move, neighbor in neighbors_function(start):            
            cost = cost_function(move, neighbor)
            #{prochaine position , orientation , [le chmemin] ,  }
            data = {'node': neighbor, 'move_list': [move], 'node_list': [neighbor]}
            
            self.neighborQueue.put((cost, next(unique), data))
    
    
    
    # Add all neighbor of a node
    def _add_neighbors(self, node, neighbors_function, cost_function):
        for move, neighbor in neighbors_function(node): 
            cost = self.top_cost + cost_function(move, neighbor)
            data = {'node': neighbor, 'move_list': self.top_data['move_list'] + [move], 'node_list': self.top_data['node_list'] + [neighbor]}
            
            self.neighborQueue.put((cost, next(unique), data))
    
    
    
    # Main function of the class
    # The start is the start of the path
    # The neighbors_function takes a node, and return a list of (move, neighbor)
    # The cost_function takes a move and a node, and return the cost of taking this node
    # The end_function takes a cost and a node, and return true is the end condition is triggered
    def find(self, start, neighbors_function, cost_function, end_function):
        # Init the queue and explored array
        self.neighborQueue = queue.PriorityQueue()
        self.explored = [False]*self.nb_cell*self.nb_cell
        self.explored[start] = True
    
        # Add first nodes
        self._first_step(start, neighbors_function, cost_function)
        
        # If no move possible return None, None
        if self.neighborQueue.empty():
            return None, None
        
        # Update the top node
        self._update_top()
        
        # While we can try new node and not finished, we iterate
        while not self.neighborQueue.empty() and not end_function(self.top_cost, self.top_data):
            node = self.top_data['node']
            
            # If the top node is not explored, explore it
            if not self.explored[node]:
                self.explored[node] = True
                self._add_neighbors(node, neighbors_function, cost_function)
                
            # Update the top node
            self._update_top()
            
        return self.top_cost, self.top_data










