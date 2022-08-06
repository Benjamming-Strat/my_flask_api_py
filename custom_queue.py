'a linked list that does first in first out inserts and removals'

class Node:
    def __init__(self, data, next_node) -> None:
        self.data = data
        self.next_node = next_node

class Queue:
    def __init__(self) -> None:
        self.head = None
        self.tail = None

    def enqueue(self, data): #adds node to our tail
        if self.tail ==  None and self.head ==None:
            self.tail = self.head = Node(data,None)
            return
        self.tail.next_node = Node(data,None)
        self.tail = self.tail.next_node
        return
    
    def dequeue(self): # removes nodes from our head
        if self.head  == None:
            return None
        removed = self.head
        self.head = self.head.next_node
        if self.head == None:
            self.tail = None
        return removed
