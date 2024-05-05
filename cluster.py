from __future__ import annotations
import json
import math
from pydoc import cli
from typing import List
import numpy as np

class Graph():
    def  __init__(self,
            nodecount : None):
        self.nodecount = nodecount
        # IMPORTANT!!!
        # Replace the next line so the Laplacian is a nodecount x nodecount array of zeros.
        # You will need to do this in order for the code to run!
        self.laplacian = np.zeros((nodecount, nodecount), dtype = int)

    # Add an edge to the Laplacian matrix.
    # An edge is a pair [x,y].
    def addedge(self,edge):
        self.laplacian[edge[0]][edge[1]] = -1
        self.laplacian[edge[1]][edge[0]] = -1
        self.laplacian[edge[0]][edge[0]] += 1
        self.laplacian[edge[1]][edge[1]] += 1
        # Nothing to return.

    # Don't change this - no need.
    def laplacianmatrix(self) -> np.array:
        return self.laplacian

    # Calculate the Fiedler vector and return it.
    # You can use the default one from np.linalg.eig
    # but make sure the first entry is positive.
    # If not, negate the whole thing.
    def fiedlervector(self) -> np.array:
        # Replace this next line with your code.
        eigenValues, eigenVector = np.linalg.eig(self.laplacian)
        value = 0
        if eigenValues[0] == 0:
            value = 1
        
        fvec = []
        for i in range(len(eigenVector[0])):
            fvec.append(eigenVector[i][value])
            
        if fvec[0] < 0:
            fvec = [ -x for x in fvec]
        # Return
        return fvec

    # Cluster the nodes.
    # You should return a list of two lists.
    # The first list contains all the indices with nonnegative (positive and 0) Fiedler vector entry.
    # The second list contains all the indices with negative Fiedler vector entry.

    def clustersign(self):
        # Replace the next two lines with your code.
        pind = []
        nind = []
        
        list = self.fiedlervector()
        
        for i in range(len(list)):
            if list[i] < 0:
                nind.append(list[i])
            else:
                pind.append(list[i])
        
        # Return
        return([pind,nind])

'''
cluster  = Graph(7)
cluster.addedge([0,5])
cluster.addedge([0,2])
cluster.addedge([2,5])
cluster.addedge([2,1])
cluster.addedge([1,4])
cluster.addedge([4,6])
cluster.addedge([6,3])
cluster.addedge([3,1])
print(cluster.laplacianmatrix())
print(cluster.fiedlervector())
print("-------")
print(cluster.clustersign())
'''
