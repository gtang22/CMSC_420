# BST Variation 1

from __future__ import annotations
import json

# The class for a particular node in the tree.
# DO NOT MODIFY!
class Node():
    def  __init__(self,
                  key        : int  = None,
                  value      : int  = None,
                  leftchild  : Node = None,
                  rightchild : Node = None):
        self.key        = key
        self.value      = value
        self.leftchild  = leftchild
        self.rightchild = rightchild

# For the tree rooted at root:
# Return the json.dumps of the list with indent=2.
# DO NOT MODIFY!
def dump(root: Node) -> str:
    def _to_dict(node) -> dict:
        return {
            "key"        : node.key,
            "value"      : node.value,
            "leftchild"  : (_to_dict(node.leftchild) if node.leftchild is not None else None),
            "rightchild" : (_to_dict(node.rightchild) if node.rightchild is not None else None)
        }
    if root == None:
        dict_repr = {}
    else:
        dict_repr = _to_dict(root)
    return json.dumps(dict_repr,indent = 2)

# For the tree rooted at root and the key and value given:
# Insert the key/value pair.
# The key is guaranteed to not be in the tree.
def insert(root: Node, key: int, value: int) -> Node:
    if root is None:
        return Node(key, value, None, None)
    elif key < root.key:
        root.leftchild = insert(root.leftchild, key, value)
    elif key > root.key:
        root.rightchild = insert(root.rightchild, key, value)
    return root

# For the tree rooted at root and the key given, delete the key.
# When replacement is necessary use the inorder successor.
def delete(root: Node, key: int) -> Node:
    parent, child = __find_node(None, root, key)
    
    if child is not None:
        if child.leftchild is None and child.rightchild is None:
            __replace_node(root, parent, child, None)
        elif child.leftchild is not None and child.rightchild is None:
            __replace_node(root, parent, child, child.leftchild)
        elif child.rightchild is not None and child.leftchild is None:
            __replace_node(root, parent, child, child.rightchild)
        else:
            newValue = __find_smallest_node(child.rightchild).key
            delete(child, newValue)
            child.key = newValue
    
    return root

def __replace_node(root: Node, parent: Node, child: Node,  node: Node):
    if parent is None:
        root = node
    elif parent.key > child.key:
        parent.leftchild = node
    else:
        parent.rightchild = node

# Returns the smallest node (the left most node)
def __find_smallest_node (root: Node):
    if root.leftchild is not None:
        return __find_smallest_node(root.leftchild)
    else:
        return root
 

def __find_node(parent: Node, child: Node, key: int):
    if child == None or child.key == key:
        return parent, child
    else:
        if child.key > key:
            return __find_node(child, child.leftchild, key)
        else:
            return __find_node(child, child.rightchild, key)

# For the tree rooted at root and the key given:
# Calculate the list of values on the path from the root down to and including the search key node.
# The key is guaranteed to be in the tree.
# Return the json.dumps of the list with indent=2.
def search(root: Node, search_key: int) -> str:
    # Remove the next line and fill in code to construct value_list.
    value_list = []
    value_list.append(root.value)
    cur = root

    while cur.key != search_key:
        if cur.key < search_key:
            cur = cur.rightchild
        elif cur.key > search_key:
            cur = cur.leftchild
            
        value_list.append(cur.value)

    return json.dumps(value_list,indent = 2)

# Restructure the tree..
def restructure(root: Node):
    inorder = __inorder_list(root, [])
    for i in range(len(inorder)):
        inorder[i].leftchild = None
        inorder[i].rightchild = None
    
    newroot = _restructure_helper(inorder, 0, len(inorder) - 1)
    return(newroot)

def _restructure_helper(list, start_index, end_index):
    if start_index > end_index:
        return None
    elif start_index == end_index:
        return list[start_index]
    else:
        middle = (end_index + start_index)//2
        newroot = list[middle]
        newroot.leftchild = _restructure_helper(list, start_index, middle - 1)
        newroot.rightchild = _restructure_helper(list, middle + 1, end_index)
        return newroot

def __inorder_list(root: Node, Node_list):
    if root is not None:
        Node_list = __inorder_list(root.leftchild, Node_list)
        Node_list.append(root)
        Node_list = __inorder_list(root.rightchild, Node_list)

    return Node_list

def print_inorder(node: Node):
    if node is not None:
        print_inorder(node.leftchild)
        print("[" + str(node.key) + "," + str(node.value) + "] ")
        print_inorder(node.rightchild)

def print_breathfirst(root: Node):
    queue = []
    queue.append(root)
    while queue:
        temp_node = queue.pop(0)
        print(temp_node.key)
        if temp_node.leftchild is not None:
            queue.append(temp_node.leftchild)
        if temp_node.rightchild is not None:
            queue.append(temp_node.rightchild)


tree1 = Node(8, 800, None, None)
tree1 = insert(tree1, 3, 300)
tree1 = insert(tree1, 10, 200)
tree1 = insert(tree1, 1, 20000)
tree1 = insert(tree1, 6, 600)
tree1 = insert(tree1, 14, 1400)
tree1 = insert(tree1, 4, 40)
tree1 = insert(tree1, 7, 700)
tree1 = insert(tree1, 13, 1300)
print_inorder(tree1)
print(search(tree1, 4))
tree1 = restructure(tree1)
print_breathfirst(tree1)
'''
tree1 = delete(tree1, 3)
print_breathfirst(tree1)
print("---")
tree1 = delete(tree1, 10)
print_breathfirst(tree1)
print("---")
tree1 = delete(tree1, 4)
print_breathfirst(tree1)
print("---")
tree1 = delete(tree1, 8)
print_breathfirst(tree1)
print("---")
print("Finished")
'''
'''
Notes for trees:

Always know when it's (), (], or []
Clear Nodes

'''