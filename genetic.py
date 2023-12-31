import random
from dought import Dought
from tqdm import tqdm
import numpy as np


def fusion(doughA, doughB):#This function is the logic of the crossover
        i, j = 1,1
        common_tuples = []
        
        while i < len(doughA.surface) and j < len(doughB.surface):
            if doughA.surface[i][0] == doughB.surface[j][0]:
                common_tuples.append(doughA.surface[i][0])  
                i += 1
                j += 1
            elif doughA.surface[i][0] < doughB.surface[j][0]:
                i += 1
            else:
                j += 1
        if len(common_tuples)==0:
            fusioned1=doughA
            fusioned2=doughB
        else:
            fusion_point=random.choice(common_tuples)
            for m, tup in enumerate(doughA.surface):
                if tup[0]==fusion_point:
                    breakA=m
            for n,tup in enumerate(doughB.surface):
                if tup[0]==fusion_point:
                    breakB=n
            new_surface1=doughA.surface[:breakA]+doughB.surface[breakB:]
            fusioned1=Dought(surface=new_surface1)
            new_surface2=doughB.surface[:breakB]+doughA.surface[breakA:]
            fusioned2=Dought(surface=new_surface2)
        return fusioned1,fusioned2


def create(dough=None):#This function creates a random valid dough
            if dough==None:
                dough=Dought()
            actions=dough.possible_actions()
            liste_action=[]
            num=0
            while len(actions)>0:
                num+=1
                action=random.choice(actions)
              
                dough.action(action)
                actions=dough.possible_actions()
                liste_action.append(action)
            
            return dough
        
def mutate(dough):#take a portion of the dough and changes it
       
        a=random.choice(dough.surface)
        b=random.choice(dough.surface)
        c=max(a,b,key=lambda x:x[0])
        d=min(a,b,key=lambda x:x[0])
      
        
        new_defects={}
        val1,val2=d[0],c[0]
        for j in dough.defects:
            if j>=val1 and j<val2:
                new_defects[j-val1+1]=dough.defects[j]
        new_dough=Dought(defects=new_defects,length=val2-val1)
        completed=create(new_dough)
        new_portion=completed.surface
   
        for i in range(len(new_portion)):
            new_portion[i]=(new_portion[i][0]+val1-1,new_portion[i][1])
        new_surface=dough.surface[:dough.surface.index(d)]+new_portion+dough.surface[dough.surface.index(c):]
        return new_surface
        



# Genetic Algorithm Class
class GeneticAlgorithm:
    def __init__(self, population_size, num_generations,mutation_rate):
        self.population_size = population_size
        self.num_generations = num_generations
        self.mutation_rate=mutation_rate
        self.population=[]
        

    def generate_initial_population(self):
        # Generate initial population
       
        
        for _ in tqdm(range(self.population_size)):
            
            individual=create()
            self.population.append(individual)
        
                

    def calculate_fitness(self, chromosome):
        # Calculate fitness using Dough.score()
        return chromosome.score()

    
    def select_parents(self):
    # Rank individuals based on fitness
        ranked_population = sorted(self.population, key=self.calculate_fitness, reverse=True)

    # Assign selection probability inversely proportional to rank
        total_individuals = len(ranked_population)
        selection_probabilities = [1.0 / (i + 1) for i in range(total_individuals)]
        total_prob = sum(selection_probabilities)
        normalized_probabilities = [prob / total_prob for prob in selection_probabilities]

    # Select parents with a probability favoring higher fitness individuals
        parents = []
        while len(ranked_population) > 1:
            parent1, parent2 = np.random.choice(ranked_population, 2, p=normalized_probabilities, replace=False)
            parents.append((parent1, parent2))
            ranked_population.remove(parent1)
            ranked_population.remove(parent2)
        # Recalculate probabilities as the population size has changed
            total_individuals = len(ranked_population)
            selection_probabilities = [1.0 / (i + 1) for i in range(total_individuals)]
            total_prob = sum(selection_probabilities)
            normalized_probabilities = [prob / total_prob for prob in selection_probabilities]

        return parents

    
    def mutation(self, individual):
       
        if random.random() < self.mutation_rate:
            return mutate(individual)
        else:
            return individual.surface
                     

    def run(self):#do the whole simulation
        best_score = float('-inf')
        best_dough = None
        self.generate_initial_population()
        print("first population created")
        for _ in tqdm(range(self.num_generations)):
            self.mutation_rate*=0.9
            new_population = []
            parents = self.select_parents()
            for parent in parents:
                child1,child2 = fusion(parent[0],parent[1])
                new_population+=[child1, child2]
            for individual in new_population:
                individual.surface=self.mutation(individual)
                
                  
            self.population = new_population
       
            for individual in self.population:
               
                score = self.calculate_fitness(individual)
                if score > best_score:
                    best_score = score
                    best_dough = individual
        return best_dough

# Example usage
ga = GeneticAlgorithm(population_size=100, num_generations=70,mutation_rate=0.06)
best_solution = ga.run()
best_solution.show()
