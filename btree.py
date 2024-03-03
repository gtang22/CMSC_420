from __future__ import annotations
import json
from typing import List

# Node Class.
# You may make minor modifications.
class Node():
    def  __init__(self,
                  keys     : List[int]  = None,
                  values   : List[str] = None,
                  children : List[Node] = None,
                  parent   : Node = None):
        self.keys     = keys
        self.values   = values
        self.children = children
        self.parent   = parent
        
    def find_node(self, key : int):
        index = -1
        for k in self.keys:
            if k == key:
                return self
            elif k > key:
                if not self.is_leaf():
                    return self.children[index + 1].find_node(key)
                else:
                    return self
            index += 1
        
        if not self.is_leaf():
            return self.children[len(self.children) - 1].find_node(key)
        else:
            return self
    
    def find_index(self, key : int):
        index = 0
        for k in self.keys:
            if k >= key:
                return index
            index += 1
            
        return -1
    
    # Splits the node and returns the new node (which contains the values greater than the median)
    def split(self, m : int):
        larger_node = Node([], [], [], self.parent)
        start = (m+1)//2
        
        while len(self.keys) > start:
            larger_node.keys.insert(0, self.keys.pop())
            larger_node.values.insert(0, self.values.pop())
            
            if not self.is_leaf():
                child = self.children.pop()
                child.parent = larger_node
                larger_node.children.insert(0, child)
        
        if not self.is_leaf():
            child = self.children.pop()
            child.parent = larger_node
            larger_node.children.insert(0, child)
    
        larger_node.leaf_sync()
        self.leaf_sync()
                   
        return larger_node
    
    def is_root(self) -> bool:
        if self.parent is None:
            return True
        return False
    
    def leaf_sync(self):
        if not self.is_leaf():
            return
        if self.children is None:
            self.children = []
        
        while len(self.children) > len(self.keys) + 1:
            self.children.pop() 
        
        while len(self.children) <= len(self.keys):
            self.children.append(None)   
        
    def is_leaf(self) -> bool:
        if self.children is None or len(self.children) == 0:
            return True
        
        for child in self.children:
            if child is not None:
                return False
        return True
    
    def is_overfull(self, m: int ) -> bool:
        if len(self.keys) >= m:
            return True
        return False
    
    def is_underfull(self, m: int) -> bool:
        if len(self.keys) < m//2:
            return True
        return False
    
    def find_biggest_keyValue(self):
        if self.is_leaf():
            return (self.keys[len(self.keys) - 1], self.values[len(self.values) - 1])
        else:
            newNode = self.children[len(self.children) - 1]
            return newNode.find_biggest_keyValue()
        
    def rotate_from_left(self, index : int , m : int):
        if not self.is_underfull(m) or self.is_root() or index <= 0:
            return False
        
        leftsib = self.parent.children[index - 1]
        half = (len(leftsib.keys) + len(self.keys))//2
        if half < m//2:
            return False
        
        while len(self.keys) < half and not leftsib.is_underfull(m):
            # Rotate the parent keys and values to self's keys and values
            tempKey = self.parent.keys[index - 1]
            tempValue = self.parent.values[index - 1]
            self.keys.insert(0, tempKey)
            self.values.insert(0, tempValue)
            # Rotate sibling key and value to parent's
            tempKey = leftsib.keys.pop()
            tempValue = leftsib.values.pop()
            self.parent.keys[index - 1] = tempKey
            self.parent.values[index - 1] = tempValue
            # Move sibling children to self
            if not leftsib.is_leaf(): 
                child = leftsib.children.pop()
                child.parent = self
                self.children.insert(0, child)
                
        leftsib.leaf_sync()
        self.leaf_sync()
        
        return not self.is_underfull(m)

    def rotate_from_right(self, index : int, m : int):
        if not self.is_underfull(m) or self.is_root() or index >= len(self.parent.children) - 1:
            return False
        
        rightsib = self.parent.children[index + 1]
        half = (len(rightsib.keys) + len(self.keys))//2
        if half < m//2:
            return False
        
        while len(self.keys) < half and not rightsib.is_underfull(m):
            # Rotate the parent keys and values to self's keys and values
            tempKey = self.parent.keys[index]
            tempValue = self.parent.values[index]
            self.keys.insert(len(self.keys), tempKey)
            self.values.insert(len(self.values), tempValue)
            # Rotate sibling key and value to parent's
            tempKey = rightsib.keys.pop(0)
            tempValue = rightsib.values.pop(0)
            self.parent.keys[index] = tempKey
            self.parent.values[index] = tempValue
            # Move sibling children to self
            if not rightsib.is_leaf():
                child = rightsib.children.pop(0)
                child.parent = self
                self.children.insert(len(self.children), child)
        
        rightsib.leaf_sync()
        self.leaf_sync()
        
        return not self.is_underfull(m)
        
    def rotate_to_left(self, index : int , m : int):
        if not self.is_overfull(m) or self.is_root() or index <= 0:
            return False
        leftsib = self.parent.children[index - 1]
        min = (len(leftsib.keys) + len(self.keys) + 1)//2
        
        while len(self.keys) > min:
            # Rotate the parent keys and values to self's keys and values
            tempKey = self.parent.keys[index - 1]
            tempValue = self.parent.values[index - 1]
            leftsib.keys.append(tempKey)
            leftsib.values.append(tempValue)
            # Rotate sibling key and value to parent's
            tempKey = self.keys.pop(0)
            tempValue = self.values.pop(0)
            self.parent.keys[index - 1] = tempKey
            self.parent.values[index - 1] = tempValue
            # Move self children to left
            if not self.is_leaf(): 
                child = self.children.pop(0)
                child.parent = leftsib
                leftsib.children.append(child)
        
        leftsib.leaf_sync()
        self.leaf_sync()
                
        return not self.is_overfull(m)
     
    def rotate_to_right(self, index : int , m : int):
        if not self.is_overfull(m) or self.is_root() or index >= len(self.parent.children) - 1:
            return False
        rightsib = self.parent.children[index + 1]
        min = (len(rightsib.keys) + len(self.keys) + 1)//2
        
        while len(self.keys) > min:
            # Rotate the parent keys and values to self's keys and values
            tempKey = self.parent.keys[index]
            tempValue = self.parent.values[index]
            rightsib.keys.insert(0, tempKey)
            rightsib.values.insert(0, tempValue)
            # Rotate sibling key and value to parent's
            tempKey = self.keys.pop()
            tempValue = self.values.pop()
            self.parent.keys[index] = tempKey
            self.parent.values[index] = tempValue
            # Move sibling children to self
            if not self.is_leaf(): 
                child = self.children.pop()
                child.parent = rightsib
                rightsib.children.insert(0, child)
        
        rightsib.leaf_sync()
        self.leaf_sync()
                
        return not self.is_overfull(m)   
          
    def merge_with_left(self, index : int, m : int):
        if not self.is_underfull(m) or self.is_root() or index <= 0:
            return False
        
        leftsib = self.parent.children[index - 1]
        half = m//2
        
        # Move parent value to left (not removing the value)
        tempKey = self.parent.keys[index - 1]
        tempValue = self.parent.values[index - 1]
        # Add the parent's value and key to left sibling 
        leftsib.keys.append(tempKey)
        leftsib.values.append(tempValue)
        
        # Add all the keys from self into list
        leftsib.keys.extend(self.keys)
        leftsib.values.extend(self.values)
        for child in self.children:
            child.parent = leftsib
        leftsib.children.extend(self.children)
        
        # Remove self from parent's children 
        self.parent.children.remove(self)
        
        # Removes parent key and value 
        self.parent.keys.pop(index - 1)
        self.parent.values.pop(index - 1)
        
        leftsib.leaf_sync()
    
        return True
        
    def merge_with_right(self, index : int, m : int):
        if not self.is_underfull(m) or self.is_root() or index >= len(self.parent.children) - 1:
            return False
        rightsib = self.parent.children[index + 1]
        half = m//2
        # Move parent value to self (not removing the value)
        tempKey = self.parent.keys[index]
        tempValue = self.parent.values[index]
        
        # Add the parent's value and key to self
        self.keys.append(tempKey)
        self.values.append(tempValue) 
        
        # Add all the keys from self into list
        self.keys.extend(rightsib.keys)
        self.values.extend(rightsib.values)
        for child in rightsib.children:
            child.parent = self
        self.children.extend(rightsib.children)
        
        # Remove self from parent's children 
        self.parent.children.remove(rightsib)
        
        # Removes parent key and value 
        self.parent.keys.pop(index)
        self.parent.values.pop(index)
        
        self.leaf_sync()
        
        return True
    
    def handle_underfull(self, m : int):
        if self.is_underfull(m) and not self.is_root():
            index = self.parent.children.index(self)

            returnval = self.rotate_from_left(index, m)
                
            if returnval is False:
                returnval = self.rotate_from_right(index, m)
            if returnval is False:
                returnval = self.merge_with_left(index, m)
            if returnval is False:
                self.merge_with_right(index, m)
            
            self.parent.handle_underfull(m)
        

# DO NOT MODIFY THIS CLASS DEFINITION.
class Btree():
    def  __init__(self,
                  m    : int  = None,
                  root : Node = None):
        self.m    = m
        self.root = root

    # DO NOT MODIFY THIS CLASS METHOD.
    def dump(self) -> str:
        def _to_dict(node) -> dict:
            return {
                "keys": node.keys,
                "values": node.values,
                "children": [(_to_dict(child) if child is not None else None) for child in node.children]
            }
        if self.root == None:
            dict_repr = {}
        else:
            dict_repr = _to_dict(self.root)
        return json.dumps(dict_repr,indent=2)

    # Insert.
    def insert(self, key: int, value: str):
        if self.root is None:
            self.root = Node([key], [value], [], None)
            self.root.leaf_sync()
        else:
            node = self.root.find_node(key)
            self._insert_helper(node, key, value, None)
                
    def _insert_helper(self, node: Node, key: int, value: str, right_child: Node):
        index = node.find_index(key)
            
        if index < 0:
            # Means key-value pair goes to the end of the list
            node.keys.append(key)
            node.values.append(value)
            if right_child is not None:
                node.children.append(right_child)
        else:
            # Insert into list
            node.keys.insert(index, key)
            node.values.insert(index, value)
            if right_child is not None:
                node.children.insert(index + 1, right_child)
    
        node.leaf_sync()
        
        if not node.is_root():
            tempIndex = node.parent.children.index(node)
            resultval = node.rotate_to_left(tempIndex, self.m)
            if not resultval:
                node.rotate_to_right(tempIndex, self.m)
        
        if node.is_overfull(self.m):
            right_node = node.split(self.m)
            median_key = node.keys.pop()
            median_value = node.values.pop()
            node.leaf_sync()
            
            if not node.is_root():
                self._insert_helper(node.parent, median_key, median_value, right_node)
            else:
                new_root = Node([median_key], [median_value], [node, right_node], None)
                node.parent = new_root
                right_node.parent = new_root
                self.root = new_root
        
    
    # Delete.
    def delete(self, key: int):
        node = self.root.find_node(key)
        self._delete_helper(node, key)
                
    def _delete_helper(self, node: Node, key: int):
        index = node.find_index(key)
        if index < 0:
            return
        
        #node with value of key exists 
        if node.is_leaf():
            node.keys.pop(index)
            node.values.pop(index)
            node.leaf_sync()
            node.handle_underfull(self.m)      
            if len(self.root.keys) == 0:
                if len(self.root.children) > 0:
                    self.root = self.root.children[0]
                    self.root.parent = None  
                else:
                    self.root = None        
        else:
            leftChild = node.children[index]
            maxKey, maxValue = leftChild.find_biggest_keyValue()
            node.keys[index] = maxKey
            node.values[index] = maxValue 
            newNode= leftChild.find_node(maxKey)
            self._delete_helper(newNode, maxKey) 
                

    # Search
    def search(self,key) -> str:
        if self.root is None:
            return []
        return self._search_helper(self.root, key, [])
    
    def _search_helper(self, node: Node, key: int, list) -> List:
        index = 0
        for k in node.keys:
            if k == key:
                list.append(k)
                list.append(node.values[index])
                return list
            elif k > key:
                if len(node.children) > index:
                    list.append(index)
                    list = self._search_helper(node.children[index], key, list)
                else:
                    return list
            index += 1
        if key > node.keys[index - 1]:
            list.append(index)
            list = self._search_helper(node.children[index], key, list)
            
        return list

