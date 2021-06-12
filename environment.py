from threading import Thread, Lock
import random

class Taquin:
    # Init the environment
    def __init__(self, n):
        #Size of the grid
        self.n = n
    
        # Dict to save data about agents (i.e: pos)
        self.agentData = {}
    
        # Mutex grid, a mutex per cell, to prevent concurency writing on same cell
        self.mutexGrid = []
        for i in range(self.n*self.n):
            self.mutexGrid.append(Lock())
        
        # Helps us to know when it's useful to print
        self.updated = True
        
        
        
    # Add an agent at the given pos, and prepare the thread of the agent
    def addAgent(self, agent, pos):
        self.agentData[agent] = {}
        self.agentData[agent]['pos'] = pos
        self.agentData[agent]['thread'] = Thread(target=agent.run, args=(), daemon=True)
    
    
    
    # Starts all the threads (activate all the agents)
    def activateAllAgent(self):
        for agent in self.agentData.keys():
            self.agentData[agent]['thread'].start()
    
    
    
    # Return the agent at the pos, if no agent at this pos return None
    def _getAgent(self, pos):
        for agent in self.agentData.keys():
            if self.agentData[agent]['pos'] == pos:
                return agent
        return None
    
    
    
    # Return the next pos' for a given pos and orientation
    def _getNextPos(self, pos, orientation):
        if orientation == 0 and pos//self.n > 0:  # NORD
            pos -= self.n
        if orientation == 1 and pos%self.n < self.n-1:  # EST
            pos += 1
        if orientation == 2 and pos//self.n < self.n-1:  # SUD
            pos += self.n
        if orientation == 3 and pos%self.n > 0:  # OUEST
            pos -= 1
        return pos
    
    
    
    # Return possible orientation for a given pos
    def _getOrientations(self, pos):
        orientations = []
        if pos//self.n > 0:  # NORD
            orientations.append(0)
        if pos%self.n < self.n-1:  # EST
            orientations.append(1)
        if pos//self.n < self.n-1:  # SUD
            orientations.append(2)
        if pos%self.n > 0:  # OUEST
            orientations.append(3)
        return orientations
    
    
    
    # Try to move an agent for a given orientation
    def moveAgent(self, agent, orientation):
        nexPos = self._getNextPos(self.agentData[agent]['pos'], orientation)
        #loc 
        self.mutexGrid[nexPos].acquire()
        try:
            #Si la case est vide
            if self._getAgent(nexPos) is None:
                self.agentData[agent]['pos'] = nexPos
                self.updated = True
        finally:
            #unlock
            self.mutexGrid[nexPos].release()
            
            
            
    # PERCEPTIONS
    #get _ position
    def perceivePosition(self, agent):
        return self.agentData[agent]['pos']
        
    #Tous les possibles prochains mouvements
    def perceiveNeighbors(self, agent, pos):
        neighbors = []
        #[orientation , positiio]
        for orientation in self._getOrientations(pos):
            neighbors.append((orientation, self._getNextPos(pos, orientation)))
        #choisir une direction aléatoire
        random.shuffle(neighbors)
        return neighbors

    #Pour savoir si pos est vide 
    def perceiveAgent(self, agent, pos):
        return self._getAgent(pos)
        
        
    
    # Display the environment
    def display(self):
        self.updated = False
    
        toPrint = ('###'*self.n + '#' + '\n')
    
        toPrint += ('+--'*self.n + '+' + '\n')
        for i in range(self.n*self.n):
            self.mutexGrid[i].acquire()
            try:
                agent = self._getAgent(i)
                toPrint += '|'
                if agent is None:
                    toPrint += ('  ')
                else:
                    toPrint += ((' ' if agent.id < 10 else '') + str(agent.id))
            finally:
                self.mutexGrid[i].release()
    
            if i%self.n == self.n-1:
                toPrint += '|\n'
                toPrint += ('+--'*self.n + '+' + '\n')

        print(toPrint, end='')

        
    
    # Return true if all agent are at the right place
    def isFinish(self):
        for agent in self.agentData.keys():
            if self.agentData[agent]['pos'] != agent.goal:
                return False
        return True
    
    
    
    # Move all agent randomly to shuffle the board
    def shuffle(self, k):
        for _ in range(k):
            for agent in self.agentData.keys():
                self.moveAgent(agent, random.randint(0, 3))










