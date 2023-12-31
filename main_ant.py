from ant import Ant,update_pher
from dought import Dought
from tqdm import tqdm
import numpy as np
import pandas as pd
defects=np.array(pd.read_csv("defects.csv"))

indice=np.argsort(defects[:,0])
defects=defects[indice]






num_ants = 10
num_iterations = 50
alpha = 1  # Influence of pheromone
beta = 1  # Influence of heuristic
evaporation_rate = 0.1


pheromons=np.ones((4,500))
dought=Dought()



ants = [Ant(dought,alpha,beta) for _ in range(num_ants)]
for iteration in tqdm(range(num_iterations)):
        pheromons=update_pher(ants,evaporation_rate,None,pheromons)
    
ant=Ant(dought,alpha,beta)
d=ant.create_dough(pheromons,defects=None)
d.show()














