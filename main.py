from environment import Taquin
import agents
from agents import AgentSimple, AgentDijkstra, AgentInteraction, AgentNegociant

import time
import matplotlib.pyplot as plt



# Lance 'nbTry' simulation, avec une grille 'size'*'size'
# 'nbAgent' agents et un timeout de 'timeout'
# Return le nombre de win, et la somme du temps de résolution
def test(size, nbAgent, display=True, nbTry=100, timeout=60):
    nbWin = 0
    sumTime = 0

    for k in range(nbTry):
        env = Taquin(size)
        for i in range(nbAgent):
            # Décommenter pour choisir le bon agent
        
            # env.addAgent(AgentSimple(i+1, i, env), i)
            # env.addAgent(AgentDijkstra(i+1, i, env), i)
            # env.addAgent(AgentInteraction(i+1, i, env), i)
            env.addAgent(AgentNegociant(i+1, i, env), i)
            
        env.shuffle(10000)
        agents.RUNNING = True
        env.activateAllAgent()
        startTime = time.time()
        
        while not env.isFinish() and time.time() - startTime < timeout:
            time.sleep(agents.DELAY/2.)
            if env.updated and display:
                env.display()
        
        if time.time() - startTime < timeout:
            nbWin += 1
        
        if display:
            env.display()
        
        sumTime += time.time() - startTime
        
        agents.RUNNING = False
        
    return nbWin, sumTime
        
        

test(5, 20, True, 1, 60)
        
        

# Procédure de teste
        
# x = []
# yWin = []
# yTime = []

# maxAgent = 24

# for i in range(maxAgent):
    # nbWin, sumTime = test(5, i+1, True, 20., 20) 
    
    # x.append(i+1)
    # yWin.append(nbWin/20.)
    # yTime.append(sumTime/20.)
    
    # if nbWin == 0:
        # break
    
    
# plt.plot(x, yWin)

# axes = plt.gca()
# plt.axis([1, maxAgent, 0, None])
# plt.ylabel('Win rate')
# plt.xlabel('Number of agents')
# plt.show()

# plt.plot(x, yTime)
# plt.axis([1, maxAgent, 0, None])
# plt.ylabel('Second')
# plt.xlabel('Number of agents')
# plt.show()
