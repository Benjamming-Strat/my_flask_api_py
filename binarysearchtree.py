from tkinter.messagebox import NO


class Node:
    def __init__(self,data=None) -> None:
        self.data = data
        self.left = None
        self.right = None

class BinarySearchTree:
    def __init__(self) -> None:
        self.root = None

    def insert(self, data):
        if self.root == None:
            self.root = Node(data)
        else:
            self._insert_recursive(data, self.root)
    
    def _insert_recursive(self, data, node):
        if data["id"] < node.data["id"]:
            if node.left == None:
                node.left = Node(data)
            else:
                self._insert_recursive(data, node.left)
        elif data["id"] > node.data["id"]:
            if node.right == None:
                node.right = Node(data)
            else:
                self._insert_recursive(data, node.right)
        else:
            return
    
    def search(self, blog_post_id):
        blog_post_id = int(blog_post_id)
        if self.root is None:
            return False
        return self._search_recursive(blog_post_id, self.root)
    
    def _search_recursive(self, blog_post_id, node):
        #if the id cannot be found 
        if node.left == None and node.right == None:
            return False
        # if the id is directly the root.node
        if blog_post_id ==  node.data["id"]:
            return node.data
        #if our blogpost_id is smaller then our node, we look in the left side of the tree until we find it
        if blog_post_id <  node.data["id"] and node.left != None:
            if blog_post_id == node.left.data["id"]:
                return node.left.data
            return self._search_recursive(blog_post_id, node.left)
        #if our blogpost_id is smaller then our node, we look in the right side of the tree until we find it
        if blog_post_id > node.data["id"] and node.right != None:
            if blog_post_id == node.right.data["id"]:
                return node.right.data
            return self._search_recursive(blog_post_id, node.right)
        return False