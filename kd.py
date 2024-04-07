from __future__ import annotations
import functools
import json
import math
from typing import List

# Datum class.
# DO NOT MODIFY.
class Datum():
    def __init__(self,
                 coords : tuple[int],
                 code   : str):
        self.coords = coords
        self.code   = code
    def to_json(self) -> str:
        dict_repr = {'code':self.code,'coords':self.coords}
        return(dict_repr)

# Internal node class.
# DO NOT MODIFY.
class NodeInternal():
    def  __init__(self,
                  splitindex : int,
                  splitvalue : float,
                  leftchild,
                  rightchild):
        self.splitindex = splitindex
        self.splitvalue = splitvalue
        self.leftchild  = leftchild
        self.rightchild = rightchild

# Leaf node class.
# DO NOT MODIFY.
class NodeLeaf():
    def  __init__(self,
                  data : List[Datum]):
        self.data = data

# KD tree class.
class KDtree():
    def  __init__(self,
                  splitmethod : str,
                  k           : int,
                  m           : int,
                  root        : NodeLeaf = None):
        self.k    = k
        self.m    = m
        self.splitmethod = splitmethod
        self.root = root

    # For the tree rooted at root, dump the tree to stringified JSON object and return.
    # DO NOT MODIFY.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            if isinstance(node,NodeLeaf):
                return {
                    "p": str([{'coords': datum.coords,'code': datum.code} for datum in node.data])
                }
            else:
                return {
                    "splitindex": node.splitindex,
                    "splitvalue": node.splitvalue,
                    "l": (_to_dict(node.leftchild)  if node.leftchild  is not None else None),
                    "r": (_to_dict(node.rightchild) if node.rightchild is not None else None)
                }
        if self.root is None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)
        
    # Insert the Datum with the given code and coords into the tree.
    # The Datum with the given coords is guaranteed to not be in the tree.
    def insert(self,point:tuple[int],code:str):
        if self.root is None:
            tempDatum = Datum(point, code)
            self.root = NodeLeaf([tempDatum])
        else:
            curNode = self.root
            prevNode = None
            # Get the node where the point should go
            while isinstance(curNode, NodeInternal):
                prevNode = curNode
                if point[prevNode.splitindex] < prevNode.splitvalue:
                    curNode = prevNode.leftchild
                else:
                    curNode = prevNode.rightchild
            
            #curNode is a NodeLeaf
            curNode.data.append(Datum(point, code))
            
            if len(curNode.data) > self.m:
                splitingIndex = 0
                splitingIndexValue = 0.0
                # spread split method getting coord
                if self.splitmethod == "spread":
                    tuple = self.get_index_max_spread(curNode.data, 0)
                    maxSpread = tuple[1] - tuple[0]
                    
                    # Get coordinate with largest spread (if =, stick with previous one)
                    for i in range(self.k):
                        temptuple = self.get_index_max_spread(curNode.data, i)
                        temp = temptuple[1] - temptuple[0]
                        if temp > maxSpread:
                            maxSpread = temp
                            splitingIndex = i
                else:
                    # alternate split method getting coord
                    if curNode is self.root:
                        splitingIndex = 0
                    else:
                        splitingIndex = (prevNode.splitindex + 1) % self.k
                        
                # Get value to split:
                # Sort the entire datum list
                self._sort_node_data(curNode, splitingIndex)
                # get the spliting value 
                half = (self.m + 1)//2
                if self.m%2 == 0:
                    splitingIndexValue = float(curNode.data[half].coords[splitingIndex])
                else:
                    splitingIndexValue = curNode.data[half].coords[splitingIndex] + curNode.data[half - 1].coords[splitingIndex]
                    splitingIndexValue = splitingIndexValue/2
                    
                # split with the index and make new Node 
                rightChild = NodeLeaf([])
                while len(curNode.data) > half:
                    temp = curNode.data.pop()
                    rightChild.data.insert(0, temp)
                    
                tempNode = NodeInternal(splitingIndex, splitingIndexValue, curNode, rightChild)
                
                # Parent points to new InternalNode
                if prevNode is None:
                    self.root = tempNode
                elif point[prevNode.splitindex] < prevNode.splitvalue:
                    prevNode.leftchild = tempNode
                else:
                    prevNode.rightchild = tempNode
                    
                
    def _sort_node_data(self, node: NodeLeaf, splitIndex):
        # rotate the coord (by turning tuple into lists) to have splitIndex in front
        # (turn lists back into tuples) afterwards
        for datum in node.data:
            tempList = list(datum.coords)
            for index in range(splitIndex):
                tempCoord = tempList.pop(0)
                tempList.append(tempCoord)
            datum.coords = tuple(tempList)

        # Sort by those coodrinates in the datums
        node.data.sort(key=functools.cmp_to_key(_compare_coords))
        
        # Unrotate back 
        for datum in node.data:
            tempList = list(datum.coords)
            for index in range(splitIndex):
                tempCoord = tempList.pop()
                tempList.insert(0, tempCoord)
            datum.coords = tuple(tempList)
            
    # With a given data list          
    def get_index_max_spread(self, list: List[Datum], index:int) -> tuple[int]:
        smallestInt = list[0].coords[index]
        largestInt = list[0].coords[index]
        
        for datum in list:
            if datum.coords[index] > largestInt:
                largestInt = datum.coords[index]
            if datum.coords[index] < smallestInt:
                smallestInt = datum.coords[index]
        
        return (smallestInt, largestInt)
            

    # Delete the Datum with the given point from the tree.
    # The Datum with the given point is guaranteed to be in the tree.
    def delete(self,point:tuple[int]):
        if self.root is not None:
            self._delete_helper(self.root, [], point, None)
               
    def _delete_helper(self, node: NodeLeaf | NodeInternal, pathNodes: list[NodeInternal], point:tuple[int], sibling: NodeInternal | NodeLeaf) -> NodeInternal:
        while isinstance(node, NodeInternal):
            pathNodes.append(node)
            if point[node.splitindex] < node.splitvalue:
                sibling = node.rightchild
                node = node.leftchild
            elif point[node.splitindex] > node.splitvalue:
                sibling = node.leftchild
                node = node.rightchild
            else:
                self._delete_helper(node.leftchild, pathNodes.copy(), point, node.rightchild)
                self._delete_helper(node.rightchild, pathNodes.copy(), point, node.leftchild)
                return 
                
        if isinstance(node, NodeLeaf):
            index = -1
            for i in range(len(node.data)):
                if node.data[i].coords == point:
                    index = i
                    break  
                  
            if index >= 0:
                node.data.pop(index)      
                if len(node.data) == 0:
                    if len(pathNodes) < 2:
                        self.root = sibling
                    else:
                        grandparent = pathNodes[-2]
                        if point[grandparent.splitindex] < grandparent.splitvalue:
                            grandparent.leftchild = sibling
                        else:
                            grandparent.rightchild = sibling        
                
    # Find the k nearest neighbors to the point.
    def knn(self,k:int,point:tuple[int]) -> str:
        # Use the strategy discussed in class and in the notes.
        # The list should be a list of elements of type Datum.
        # While recursing, count the number of leaf nodes visited while you construct the list.
        # The following lines should be replaced by code that does the job.
        leaveschecked = 0
        knnlist = []
        knndistancelist = []
        # The following return line can probably be left alone unless you make changes in variable names.
        
        # Find the closest leaf to the point
        if self.root is None:
            return ""
        else:
            leaveschecked = self._knn_helper(k, point, knnlist, knndistancelist, self.root, 0)
            knnlist.sort(key=functools.cmp_to_key(_compare_coords))
            
                
        return(json.dumps({"leaveschecked":leaveschecked,"points":[datum.to_json() for datum in knnlist]},indent=2))

    def _knn_helper(self, k: int, point:tuple[int], knnlist: list, knndistancelist: list, node: NodeInternal | NodeLeaf, 
                    leaveschecked: int) -> int:
        if isinstance(node, NodeLeaf):
            for datapoint in node.data:
                if len(knnlist) < k:
                    # If the list isn't full, add the point to knnList
                    knnlist.append(datapoint)
                    knndistancelist.append(distance_between_points(datapoint.coords, point))
                else:
                    # If the list is full, replace the furthest point if this one is closer
                    largestPointIndex = self._find_largest_index(knndistancelist)
                    
                    tempdist = distance_between_points(datapoint.coords, point)
                    if tempdist < knndistancelist[largestPointIndex]:
                        knnlist[largestPointIndex] = datapoint
                        knndistancelist[largestPointIndex] = tempdist
                    elif tempdist == knndistancelist[largestPointIndex]:
                        if datapoint.code < knnlist[largestPointIndex].code:
                            knnlist[largestPointIndex] = datapoint
                            knndistancelist[largestPointIndex] = tempdist
                            
            return leaveschecked + 1
        else:
            if node.leftchild is not None and node.rightchild is not None:
                # both subtrees exist
                leftboundingbox = self._get_bounding_box(node.leftchild)
                rightboundingbox = self._get_bounding_box(node.rightchild)
                
                if self._distance_to_bounding_box(point, leftboundingbox) < self._distance_to_bounding_box(point, rightboundingbox):
                    leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.leftchild, leaveschecked)
                    leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.rightchild, leaveschecked)
                else:
                    leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.rightchild, leaveschecked)
                    leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.leftchild, leaveschecked)
            elif node.leftchild is not None:
                leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.leftchild, leaveschecked)
            elif node.rightchild is not None:
                leaveschecked = self._visit_child(k, point, knnlist, knndistancelist, node.rightchild, leaveschecked)        
            return leaveschecked
        
    def _visit_child(self, k: int, point:tuple[int], knnlist: list, knndistancelist: list, child: NodeInternal | NodeLeaf, 
                    leaveschecked: int) -> int:
        if len(knnlist) < k:
            leaveschecked = self._knn_helper(k, point, knnlist, knndistancelist, child, leaveschecked)
        else:
            boundingbox = self._get_bounding_box(child)
            if self._distance_to_bounding_box(point, boundingbox) <= knndistancelist[self._find_largest_index(knndistancelist)]:
                leaveschecked = self._knn_helper(k, point, knnlist, knndistancelist, child, leaveschecked)
        
        return leaveschecked
            
    def _find_largest_index(self, distanceList: list):
        largestPointIndex = 0
        for i in range(len(distanceList)):
                        if distanceList[i] > distanceList[largestPointIndex]:
                            largestPointIndex = i
        return largestPointIndex    
    
    # boundingbox: [[xmin, ymin, zmin], [xmax, ymax, zmax]]
    def _get_bounding_box_for_leaf(self, leaf: NodeLeaf):
        minlist = []
        maxlist = []
        
        for i in range(self.k):
            tempTuple = self.get_index_max_spread(leaf.data, i)
            minlist.append(tempTuple[0])
            maxlist.append(tempTuple[1])
        
        return [minlist, maxlist]

    def merge_bounding_boxes(self, box1: List, box2: List):
        minlist = []
        maxlist = []
        
        for i in range(self.k):
            minimum = min(box1[0][i], box2[0][i])
            minlist.append(minimum)
            maximum = max(box1[1][i], box2[1][i])
            maxlist.append(maximum)
            
        return [minlist, maxlist]
        
    def _get_bounding_box(self, subtree: NodeInternal | NodeLeaf):
        if isinstance(subtree, NodeLeaf):
            return self._get_bounding_box_for_leaf(subtree)
        else:
            if subtree.leftchild is not None and subtree.rightchild is not None:
                return self.merge_bounding_boxes(self._get_bounding_box(subtree.leftchild), self._get_bounding_box(subtree.rightchild))
            elif subtree.leftchild is None:
                return self._get_bounding_box(subtree.rightchild)
            else:
                return self._get_bounding_box(subtree.leftchild)
    
    def _distance_to_bounding_box(self, point: tuple[int], boundingBox: List):
        distance = 0
        
        for i in range(self.k):
            if point[i] < boundingBox[0][i]:
                distance += (point[i] - boundingBox[0][i]) ** 2
            elif point[i] > boundingBox[1][i]:
                distance += (boundingBox[1][i] - point[i]) ** 2
                
        return distance
    
def distance_between_points(point1: tuple[int], point2: tuple[int]):
    distance = 0
    
    for i in range(len(point1)):
        distance += (point1[i] - point2[i]) ** 2
    
    return distance 
    
def _compare_coords(datum1: Datum, datum2: Datum):
    for index in range(len(datum1.coords)):
        if datum1.coords[index] > datum2.coords[index]:
            return 1
        elif datum1.coords[index] < datum2.coords[index]:
            return  -1
    return 0
    
'''
kdTree = KDtree("spread", 3, 3)
kdTree.insert((4,4,3), "WXZ")
kdTree.insert((17,0,2), "SAX")
kdTree.insert((6,5,16), "SAX")
kdTree.insert((7,19,11), "SAX")
kdTree.insert((19,10,10), "SAX")
kdTree.insert((18,18,0), "SAX")
kdTree.insert((5,12,13), "SAX")
kdTree.insert((0,6,17), "SAX")
kdTree.insert((16,16,12), "SAX")
kdTree.insert((15,15,15), "SAX")
kdTree.delete((18, 18, 0))
kdTree.delete((17, 0, 2))

kdTree2.delete((16, 19, 18))
'''


