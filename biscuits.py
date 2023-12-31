


class Biscuit:
        def __init__(self,categorie):
            self.categorie=categorie
            if categorie==0:
                
                self.length=4
                self.value=6
                self.accept={'a': 4, 'b':2, 'c' : 3}
            elif categorie==1:
                self.length=8
                self.value=12
                self.accept={'a':5,'b':4,'c':4}
            elif categorie==2:
                self.length=2
                self.value=1
                self.accept={'a':1,'b':2,'c':1}
            elif categorie==3:
                self.length=5
                self.value=8
                self.accept={'a':2,'b':3,'c':2}
            self.heuristic=self.value/self.length
            
