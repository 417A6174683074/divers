import pandas as pd
import numpy as np
import random
from biscuits import Biscuit
defects=np.array(pd.read_csv("defects.csv"))

indice=np.argsort(defects[:,0])
defects=defects[indice]



class Dought:
    def __init__(self,surface=None,defects=None,length=500):
        self.length=length
        #Create a dictionnary of all the step and in this 
        #dictionnaty we put a dictionnary of the number of 'a', 'b' and 'c' defects per steps
        if defects is None:
            defects=np.array(pd.read_csv("defects.csv"))

            indice=np.argsort(defects[:,0])
            defects=defects[indice]
            self.defects={}
            indice=0
            for i in range(1,length+1):
                self.defects[i]={'a':0,'b':0,'c':0}
                while indice<self.length and int(defects[indice][0])+1==i:
                    self.defects[i][defects[indice][1]]+=1
                    indice+=1
        else:
            self.defects=defects
            
        
        self.done=False
        if surface is None:
            self.surface=[]
        else:
            self.surface=surface #memory of the biscuit we posed
        self.lengths={0:4,1:8,2:2,3:5}
        self.scores={0:6,1:12,2:1,3:8}
        
        

        
    def available(self,biscuit):#gives any starting spot for a biscuit of type biscuit
        i=1
        j=self.length
        available=[]
        for k in self.surface:
            if k[0]-i>=biscuit.length:
                for w in range(i,k[0]+1-biscuit.length):
                    if self.possible(biscuit.categorie,w):
                        available.append((i,biscuit.categorie))
        #    print(self.surface)
            i=k[0]+self.lengths[k[-1]]
        if j-i>biscuit.length:
            
            for w in range(i,j+1-biscuit.length):
                if self.possible(biscuit.categorie,w):
                    available.append((w,biscuit.categorie))
                    #print((w,biscuit.categorie))
        
        return available
            
            
    def possible_actions(self):# gives a list of all possible actions (possible place for any possible biscuit)
        possible=[]
        bisc_cat=[0,1,2,3]
        for i in bisc_cat:
            bisc=Biscuit(i)
            a=self.available(bisc)
         
            possible+=a
        if len(possible)==0:
            self.done=True
        return possible
    
    def show(self):
        score=0
        for i in self.surface:
            x,y=i
            end=x+self.lengths[y]-1
            score+=self.scores[y]
            print(f"one biscuit from {x} to {end} of type {y}")
        print(f"we have a score of {score}")
            
        #500
        
    def action(self,action):# make the action of putting a biscuit (registred in the surface variable)
        start,categorie=action

        pose=False
        for i in range(len(self.surface)):
            if self.surface[i][0]>start:
                pose=True
                self.surface.insert(i,(start,categorie))
                break
        if len(self.surface)==0:
            self.surface.append(action)
            pose=True
        if not pose:
            self.surface.append(action)
       


    def possible(self,bisc,x):#this function takes in argument a biscuit types, and a spot x,
    #it returns True if we can put such a biscuit here and if not false.
        
        
        
        k=0
 #       print(x,self.surface[k][0],self.surface[k][-1])
        #print(self.surface)
       
        end=self.lengths[bisc]+x-1
        if end>self.length:
        #    print('f')
            return False
        #print(self.surface)
        if len(self.surface)>0:
           # print(k,self.surface)
            forbidden=[i for i in range(x,end+1)]
            while k<len(self.surface) and self.surface[k][0]<=end:
             #   print(self.surface[k])
            
                Kend=self.surface[k][0]+self.lengths[self.surface[k][-1]]-1
                #print(bisc,x)
                if self.surface[k][0] in forbidden or Kend in forbidden or x in [i for i in range(self.surface[k][0],Kend)]:
         #           print('h')
                #    print('superposition error')
                    return False
                k+=1
        biscuit=Biscuit(bisc)
        a_limit=biscuit.accept['a']
        b_limit=biscuit.accept['b']
        c_limit=biscuit.accept['c']
        
        Ascore=0
        Bscore=0
        Cscore=0
        for j in range(x,end+1):
            Ascore+=self.defects[j]['a']
            Bscore+=self.defects[j]['b']
            Cscore+=self.defects[j]['c']
        if Ascore>a_limit or Bscore>b_limit or Cscore>c_limit:
          #  print('nop')
           # print("defect error")
            return False
        #print('yep')
        return True
        
    def all_possibles(self):# return the number of possible biscuit (combinaisons of spot and types)
        count=0
        for bisc in range(4):
            for x in range(self.length):
                if self.possible(bisc,x):
                    count+=1
        return count
            
    def score(self):#This function gives the finale score of a dough
        score=0
        for i in self.surface:
            x,y=i
            score+=self.scores[y]
        return score
    
 
    
        
        
        
            
        





    
    
            
            