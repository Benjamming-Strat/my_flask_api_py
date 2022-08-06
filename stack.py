'a stack is a linked list with last in first out  insertions and removals order'
class Node:
    def __init__(self, data, next_node) -> None:
        self.data = data
        self.next_node = next_node

class Stack:
    def __init__(self) -> None:
        self.top = None
    
    def peek(self):#see what our top is
        return self.top

    def push(self, data): #insert nodes to stack
        next_node = self.top
        new_top = Node(data, next_node)
        self.top = new_top

    def pop(self):
        if self.top == None:
            return None
        removed = self.top
        self.top = self.top.next_node
        return removed