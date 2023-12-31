import numpy as np
import random
from biscuits import Biscuit
from dought import Dought


pheromons=np.ones((4,500))



class Ant:
    def __init__(self,probl,alpha=1,beta=1):
        #self.pheromons=np.ones((4,500))
        self.prob=probl
        self.alph=alpha
        self.bet=beta
        self.heuristic_values=[Biscuit(i).heuristic for i in range(4)]
        
    def proba(self,bisc,x,pheromons):#returns the probabilty that we start a biscuit of type bisc at x
        if not self.prob.possible(bisc,x):
           
            return 0
        pherom=pheromons[bisc][x-1]
        heur=self.heuristic_values[bisc]
      
       
        attract=(pherom**self.alph)*(heur**self.bet)
        a=[]
        for i in range(4):
         
            if self.prob.possible(i,x):
                a.append(i)
       
        normalization=sum((pheromons[i][x-1]**self.alph)*(self.heuristic_values[i]**self.bet) for i in a)
       
        proba=attract/normalization if normalization>0 else 0
        return proba
        
    def choose_bisc(self,x,pheromons):#return the chosen biscuit types  according to all the 
    #probability computed with the previous function
        prob=[]
      
        for bisc_type in range(4):
            proba=self.proba(bisc_type,x,pheromons)
            prob.append((proba,bisc_type))
          
        tot_prob=sum(p[0] for p in prob)
        if tot_prob==0:
            return -1
        normalized_prob=[(p[0]/tot_prob,p[1]) for p in prob]
        choice = random.choices(normalized_prob, weights=[p[0] for p in normalized_prob], k=1)[0]

        return choice[1]
    
    
    
    def create_dough(self,pheromons,defects):
        #create a dought that is filled with biscuit chosen according to the probability function
        self.prob=Dought(defects)
        a=0
        while len(self.prob.surface)==0 or ((not self.prob.done) and self.prob.all_possibles()>0):
            if len(self.prob.surface)==0:
                x=1
            else:
                x= self.prob.surface[-1][0]+  self.prob.lengths[self.prob.surface[-1][-1]]+a
                
           
            num=self.choose_bisc(x,pheromons)
            if num==-1:
                a+=1
                continue
            else:
                a=0
           
            self.prob.surface.append((x,num))
        return self.prob
        
def update_pher(ants,evaporation_rate,defects,pheromons=pheromons):
    #This function is central, it takes several ants and make them create dought following
    #our probabilistic logic, then it actualise the pheromon matrix according to our formula
    pheromons*=(1-evaporation_rate)
    flag=np.zeros((4,500))
    pher_bis=np.zeros((4,500))
    for ant in ants:
        d=ant.create_dough(pheromons,defects)
        for bisc in d.surface:
            start,typ=bisc
            b=Biscuit(typ)
            end=start+b.length-1
            score=d.score()
          
            pher_bis[typ,start:end+1]+=score
            #flag[typ,start:end+1]+=1
    for y in range(4):
        for x in range(500):
            if flag[y,x]>1:#keep proportions between the node that apears multiple times and those who appears a single time
                pher_bis[y,x]/=flag[y,x]
    norma_bis=np.max(pher_bis)
    pher_bis/=norma_bis
    pheromons+=pher_bis
               
            
    return pheromons
        
        
        
        
        
        
'''        
    def theta(self,cat1,cat2,x1,x2):
        theta=self.pheromons[cat2][x2-1]/self.pheromons[cat1][x1-1]
        return theta
        
    def prob(self,x,y):#gives the probability that we use a x type biscuit
        bisc,x=x
        biscY,x2=y
        poss=[]
        if not self.probl.possible(y):
            return 0
        for i in range(4):
            if self.probl.possible((i,x1)):
                poss.append(Biscuit(i))
        
        theta=self.theta(biscX.categorie,biscY.categorie,x1,x2)
        heta=np.exp(biscY.value-biscX.value)
        denom=sum((self.theta(biscX.categori,biscZ.categorie,x1,x1)**self.alph)*
                      (np.exp(biscZ.value-biscX.value)**self.bet) for biscZ in poss)
        p=(theta**self.alph)*(heta**self.bet)/denom    
        return p
'''    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
            