from dijkstra import Dijkstra

import time
import random
import queue

RUNNING = True
DELAY = 0.001



class AgentSimple:
    def __init__(self, id, goal, env):
        self.id = id
        self.goal = goal
        self.env = env
    
    
    
    def run(self):
        while RUNNING:
            time.sleep(DELAY)
            pos = self.env.perceivePosition(self)
            if pos == self.goal:
                break
            
            if random.randint(0, 1) == 0:  # Focus x axis
                if self.goal%self.env.n < pos%self.env.n:
                    self.env.moveAgent(self, 3)
                elif self.goal%self.env.n > pos%self.env.n:
                    self.env.moveAgent(self, 1)
            else:
                if self.goal//self.env.n < pos//self.env.n:
                    self.env.moveAgent(self, 0)
                elif self.goal//self.env.n > pos//self.env.n:
                    self.env.moveAgent(self, 2)



class AgentDijkstra:
    def __init__(self, id, goal, env):
        self.id = id
        self.goal = goal
        self.env = env
        self.dijkstra = Dijkstra(env.n*env.n)
    
    
    
    def run(self):
        while RUNNING:
            time.sleep(DELAY)
            pos = self.env.perceivePosition(self)
            if pos == self.goal:
                break
            
            
            dijkstra_cost, dijkstra_data = self.dijkstra.find(
                pos,
                lambda neighbors_function: self.env.perceiveNeighbors(self, node),
                lambda cost_function, neighbor: 1 if self.env.perceiveAgent(self, neighbor) is None else 1000,
                lambda end_function, data: data['node'] == self.goal
            )
            
            self.env.moveAgent(self, dijkstra_data['move_list'][0])

            
            
#juste move messages 
class AgentInteraction:
    def __init__(self, id, goal, env):
        self.id = id
        self.goal = goal
        self.env = env
        self.message_queue = queue.Queue()
        self.dijkstra = Dijkstra(env.n*env.n)
    
    
    
    def send_message(self, to, message):
        # print(self.id, 'SEND_TO', to.id, message)
        message['author'] = self
        to.message_queue.put(message)
    
    
    
    def read_message(self):
        self.has_to_move = False
    
        while not self.message_queue.empty():
            message = self.message_queue.get()
            # print(self.id, 'READ_FROM', message['author'].id, message)
            
            if message['type'] == 'MOVE':
                self.has_to_move = True
     


    def run(self):
        while RUNNING:
            time.sleep(DELAY)    
            self.has_to_move = True(DELAY)
            self.read_message()
            pos = self.env.perceivePosition(self)
            # print(self.id, pos, self.goal, self.state, self.state_data)
            
            if self.has_to_move:
                move, neighbor = random.choice(self.env.perceiveNeighbors(self, pos))
                
                #Check if nextPosition is empty
                next_node_agent = self.env.perceiveAgent(self, neighbor)
                    
                if next_node_agent is None:
                    self.env.moveAgent(self, move)
                else:
                    self.send_message(next_node_agent, {'type': 'MOVE'})
            else:            
                dijkstra_cost, dijkstra_data = self.dijkstra.find(
                    pos,
                    lambda node: self.env.perceiveNeighbors(self, node),
                    lambda move, neighbor: 1 if self.env.perceiveAgent(self, neighbor) is None else 1000,
                    lambda cost, data: data['node'] == self.goal
                )

                next_node_agent = self.env.perceiveAgent(self, dijkstra_data['node_list'][0])
                    
                if next_node_agent is None:
                    self.env.moveAgent(self, dijkstra_data['move_list'][0])
                else:
                    self.send_message(next_node_agent, {'type': 'MOVE'})
            
               
               
class AgentNegociant:
    def __init__(self, id, goal, env):
        self.id = id
        self.goal = goal
        self.env = env
        self.message_queue = queue.Queue()
        self.dijkstra = Dijkstra(env.n*env.n)
        
        self.state = 'TRY_PATH'
        self.state_data = {}
    
    
    
    def send_message(self, to, message):
        # print(self.id, 'SEND_TO', to.id, message)
        message['author'] = self
        to.message_queue.put(message)
    
    
    
    def read_message(self):
        best_value = None
        best_message = None
    
        while not self.message_queue.empty():
            message = self.message_queue.get()
            # print(self.id, 'READ_FROM', message['author'].id, message)
            
            if message['type'] == 'MOVE':
                if best_value is None or best_value > message['value']:
                    if best_value is not None:
                        self.send_message(best_message['author'], {
                            'type': 'NO'
                        })
                
                    best_value = message['value']
                    best_message = message
                else:
                    self.send_message(message['author'], {
                        'type': 'NO'
                    })
            
            if message['type'] == 'NO':
                if self.state == 'TRY_PATH_WAIT_MOVE' and self.state_data['from'] == message['author']:
                    self.state = 'TRY_PATH'
                    
                if self.state == 'TRY_MOVE_WAIT_MOVE' and self.state_data['from'] == message['author']:
                    self.state = 'TRY_PATH'
                    ###################################################
                    self.send_message(self.state_data['for'], {
                        'type': 'NO'
                    })
            
            if message['type'] == 'YES':
                
                if self.state == 'TRY_PATH_WAIT_MOVE' and self.state_data['from'] == message['author']:
                    self.state = 'TRY_PATH'
                
                    self.env.moveAgent(self, self.state_data['next_move'])
                    
                    self.send_message(self.state_data['from'], {
                        'type': 'THX'
                    })
                    
                if self.state == 'TRY_MOVE_WAIT_MOVE' and self.state_data['from'] == message['author']:
                    self.state = 'TRY_MOVE_WAIT_THX'
                    
                    self.env.moveAgent(self, self.state_data['next_move'])
                    
                    self.send_message(self.state_data['for'], {
                        'type': 'YES'
                    })

            if message['type'] == 'THX':
                if self.state == 'TRY_MOVE_WAIT_THX' and self.state_data['for'] == message['author']:
                    self.state = 'TRY_PATH'
                    
                    if 'from' in self.state_data.keys():
                        self.send_message(self.state_data['from'], {
                            'type': 'THX'
                        })
    
        return best_value, best_message
     


    def run(self):
        while RUNNING:
            time.sleep(DELAY)
            best_value, best_message = self.read_message()
            #APOSITION ACTUELLE
            pos = self.env.perceivePosition(self)
            # print(self.id, pos, self.goal, self.state, self.state_data)
            
            if self.state == 'TRY_PATH':
                dijkstra_cost, dijkstra_data = self.dijkstra.find(
                    pos,
                    lambda node: self.env.perceiveNeighbors(self, node),
                    lambda move, neighbor: 1 if self.env.perceiveAgent(self, neighbor) is None else 1000,
                    lambda cost, data: data['node'] == self.goal
                )
                
                self.state_data = {}
                self.state_data['distance_to_goal'] = len(dijkstra_data['move_list'])
                self.state_data['next_move'] = dijkstra_data['move_list'][0]
                self.state_data['next_node'] = dijkstra_data['node_list'][0]
                #Top neighbor , movliste
                self.state_data['plan'] = dijkstra_data['node_list'][:2]
            
                if best_value is not None and (pos == self.goal or self.state_data['distance_to_goal'] >= best_value):
                    self.state = 'TRY_MOVE'
                    self.state_data = {}
                    self.state_data['for'] = best_message['author']
                    self.state_data['value'] = best_message['value']
                    self.state_data['forbiden'] = best_message['forbiden']

                else:
                    if best_value is not None:
                        self.send_message(best_message['author'], {
                            'type': 'NO'
                        })
                
                    if pos != self.goal:
                        next_node_agent = self.env.perceiveAgent(self, self.state_data['next_node'])
                            
                        if next_node_agent is None:
                            self.env.moveAgent(self, self.state_data['next_move'])
                        else:
                            self.state = 'TRY_PATH_WAIT_MOVE'
                            self.state_data['from'] = next_node_agent
                        
                            self.send_message(next_node_agent, {
                                'type': 'MOVE',
                                'value': self.state_data['distance_to_goal'],
                                'forbiden': [pos] + self.state_data['plan']
                            })
            
            if self.state == 'TRY_MOVE':
                dijkstra_cost, dijkstra_data = self.dijkstra.find(
                    pos,
                    lambda node: [x for x in self.env.perceiveNeighbors(self, node) if x[1] not in self.state_data['forbiden']],
                    lambda neighbors_function, neighbor: 1 if self.env.perceiveAgent(self, neighbor) is None else 1000,
                    lambda cost, data: self.env.perceiveAgent(self, data['node']) is None
                )
                
                if dijkstra_cost is None:
                    self.state = 'TRY_PATH'
                    
                    #Impossible de bouger malgré ton bon plan
                    self.send_message(self.state_data['for'], {
                        'type': 'NO'
                    })
                else:
                    self.state_data['next_move'] = dijkstra_data['move_list'][0]
                    self.state_data['next_node'] = dijkstra_data['node_list'][0]
                    
                    next_node_agent = self.env.perceiveAgent(self, self.state_data['next_node'])
                    
                    if next_node_agent is None:
                        self.state = 'TRY_MOVE_WAIT_THX'
                    
                        self.env.moveAgent(self, self.state_data['next_move'])

                        self.send_message(self.state_data['for'], {
                            'type': 'YES'
                        })
                    else:
                        self.state = 'TRY_MOVE_WAIT_MOVE'
                        self.state_data['from'] = next_node_agent
                    
                        self.send_message(next_node_agent, {
                            'type': 'MOVE',
                            'value': self.state_data['value'],
                            'forbiden': [pos] + self.state_data['forbiden']
                        })
            else:
                if best_value is not None:
                    self.send_message(best_message['author'], {
                        'type': 'NO'
                    })










