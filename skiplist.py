from __future__ import annotations
import copy
import json
import math
from typing import List

verbose = False

# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key      : int,
                  value    : str,
                  toplevel : int,
                  pointers : List[Node] = None):
        self.key      = key
        self.value    = value
        self.toplevel = toplevel
        self.pointers = pointers

# DO NOT MODIFY!
class SkipList():
    def  __init__(self,
                  maxlevel : int = None,
                  nodecount: int = None,
                  headnode : Node = None,
                  tailnode : Node = None):
        self.maxlevel = maxlevel
        self.nodecount = nodecount
        self.headnode  = headnode
        self.tailnode  = tailnode

    # DO NOT MODIFY!
    # Return a reasonable-looking json.dumps of the object with indent=2.
    # We create an list of nodes,
    # For each node we show the key, the value, and the list of pointers and the key each points to.
    def dump(self) -> str:
        currentNode = self.headnode
        nodeList = []
        while currentNode is not self.tailnode:
            pointerList = str([n.key for n in currentNode.pointers])
            nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
            currentNode = currentNode.pointers[0]
        pointerList = str([None for n in currentNode.pointers])
        nodeList.append({'key':currentNode.key,'value':currentNode.value,'pointers':pointerList})
        return json.dumps(nodeList,indent = 2)

    # DO NOT MODIFY!
    # Creates a pretty rendition of a skip list.
    # It's vertical rather than horizontal in order to manage different lengths more gracefully.
    # This will never be part of a test but you can put "pretty" as a single line in your tracefile
    # to see what the result looks like.
    def pretty(self) -> str:
        currentNode = self.headnode
        longest = 0
        while currentNode != None:
            if len(str(currentNode.key)) > longest:
                longest = len(str(currentNode.key))
            currentNode = currentNode.pointers[0]
        longest = longest + 2
        pretty = ''
        currentNode = self.headnode
        while currentNode != None:
            lineT = 'Key = ' + str(currentNode.key) + ', Value = ' + str(currentNode.value)
            lineB = ''
            for p in currentNode.pointers:
                if p is not None:
                    lineB = lineB + ('('+str(p.key)+')').ljust(longest)
                else:
                    lineB = lineB + ''.ljust(longest)
            pretty = pretty + lineT
            if currentNode != self.tailnode:
                pretty = pretty + "\n"
                pretty = pretty + lineB + "\n"
                pretty = pretty + "\n"
            currentNode = currentNode.pointers[0]
        return(pretty)

    # DO NOT MODIFY!
    # Initialize a skip list.
    # This constructs the headnode and tailnode each with maximum level maxlevel.
    # Headnode has key -inf, and pointers point to tailnode.
    # Tailnode has key inf, and pointers point to None.
    # Both have value None.
    def initialize(self,maxlevel):
        pointers = [None] * (1+maxlevel)
        tailnode = Node(key = float('inf'),value = None,toplevel = maxlevel,pointers = pointers)
        pointers = [tailnode] * (maxlevel+1)
        headnode = Node(key = float('-inf'),value = None, toplevel = maxlevel,pointers = pointers)
        self.headnode = headnode
        self.tailnode = tailnode
        self.maxlevel = maxlevel

    # Create and insert a node with the given key, value, and toplevel.
    # The key is guaranteed to not be in the skiplist.
    # Check if we need to rebuild and do so if needed.
    def insert(self,key,value,toplevel):
        if (self.headnode is None):
            self.initialize(self.maxlevel)
        
        if (self.nodecount is None):    
            self.nodecount = 0
            
        cur = self.headnode
        level = self.maxlevel
        prevPointers = []
        # Find position for new node
        while (cur.key != key and level >= 0):
            nextkey = cur.pointers[level].key
            if (nextkey > key):
                prevPointers.insert(0, cur)
                level -= 1
            else:
                cur = cur.pointers[level]
        
        # Create new node
        tempNode = Node(key, value, toplevel, [])
        
        # Insert new node
        for i in range(toplevel + 1):
            tempNode.pointers.append(prevPointers[i].pointers[i])
            prevPointers[i].pointers[i] = tempNode
        
        self.nodecount += 1
        # If the expected maximum height number of nodes > skip list's maximum 
        # enforced level rebuild
        emh = math.log(self.nodecount, 2) + 1
        if (emh > self.maxlevel):
            # Rebuild into perfect skiplist
            hn = self.headnode
            nodeCount = self.nodecount
            # double height
            self.initialize(self.maxlevel * 2)
            self.nodecount = 0
            
            count = 1
            oldCur = hn.pointers[0]
            for i in range(nodeCount):
                height = self.__find_highest_power_of_2(count, 2, 0)
                self.insert(oldCur.key, oldCur.value, height)
                oldCur = oldCur.pointers[0]
                count+= 1
        
    
    def __find_highest_power_of_2(self, num: int, twoPow: int, count: int):
        if (num % twoPow != 0):
            return count
        return self.__find_highest_power_of_2(num, twoPow * 2, count + 1)
        
    
    # Delete node with the given key.
    # The key is guaranteed to be in the skiplist.
    def delete(self,key):
        # Find the Node with the key given
        cur = self.headnode
        prevPointers = []
        level = self.maxlevel
        # Find node 
        while (cur.key != key and level >= 0):
            nextkey = cur.pointers[level].key
            if (nextkey > key):
                level -= 1
            else:
                cur = cur.pointers[level]
        
        mylevel = cur.toplevel
        
        # Record pointers to the node 
        for i in range(mylevel + 1):
            current = self.headnode
            while(current.pointers[i] is not None and current.pointers[i].key != key):
                current = current.pointers[i]
            prevPointers.append(current)
        
        # Move pointers to ignore node      
        for i in range(mylevel + 1):
            prevPointers[i].pointers[i] = cur.pointers[i]
        
        # Remove one from node count
        self.nodecount -= 1

    # Search for the given key.
    # Construct a list of all the keys in all the nodes visited during the search.
    # Append the value associated to the given key to this list.
    def search(self,key) -> str:
        A = []
        
        cur = self.headnode
        level = self.maxlevel
        
        # Go to find the value, if not exists, level will be -1
        while (cur.key != key and level >= 0):
            nextkey = cur.pointers[level].key
            if (nextkey > key):
                level -= 1
            else:
                A.append(cur.key)
                cur = cur.pointers[level]
        
        if (level != -1):
            A.append(cur.key)  
            A.append(cur.value)  
        
        return json.dumps(A,indent = 2)

