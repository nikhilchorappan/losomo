import sys
import numpy as np
from scipy.linalg import eig  
from scipy.cluster.vq import kmeans2

class sgraph:
     def __init__(self,AdjacencyMatrix):
         self.W = AdjacencyMatrix

     def __rename_clusters(self,idx):  
         # so that first cluster has index 0  
         num = -1  
         seen = {}  
         newidx = []  
         for id in idx:  
             if id not in seen:  
                 num += 1  
                 seen[id] = num  
             newidx.append(seen[id])  
         return np.array(newidx)  

     def getcluster(self,n):
          G = np.diag([sum(Wi) for Wi in self.W])
          L = self.W - G

          # sparse eigen is a little bit faster than eig  
          evals, evcts = eig(L)  
          evals, evcts = evals.real, evcts.real  
          edict = dict(zip(evals, evcts.transpose()))  
          evals = sorted(edict.keys())

          # second and third smallest eigenvalue + vector  
          Y = np.array([edict[k] for k in evals[1:3]]).transpose()  
          res, idx = kmeans2(Y, n,  iter = 1000, minit='random')  
          return self.__rename_clusters(idx) 



def main(args):    
    W = np.array([[ 0,  1,  1,  1,  0,  0,  0,  0],
                  [ 1,  0,  1,  1,  0,  0,  0,  0],
                  [ 1,  1,  0,  1,  0,  0,  0,  0],
                  [ 1,  1,  1,  0,  0,  0,  0,  0],     
                  [ 0,  0,  0,  0,  0,  1,  1,  1],
                  [ 0,  0,  0,  0,  1,  0,  1,  1],
                  [ 0,  0,  0,  0,  1,  1,  0,  1],
                  [ 0,  0,  0,  0,  1,  1,  1,  0],])

    G =  sgraph(W)
    print G.getcluster()

if __name__ == "__main__":  
    main(sys.argv) 
