from readline import insert_text


class Node:
    def __init__(self, data = None, next_node=None) -> None:
        self.data = data
        self.next_node = next_node

class Linked_list():
    def __init__(self) -> None:
        self.head = None
        self.last_node = None

    def print_ll(self):
        ll_string = ""
        node = self.head
        if node is None:
            print(None)
        while node:
            ll_string += f" {str(node.data)}"              
            node = node.next_node
        ll_string += " None"
        
    
    def insert_beginning(self, data):
        if self.head is None:
            self.head = Node(data, None)
            self.last_node = self.head

        new_node = Node(data, self.head)
        self.head = new_node
    
    def insert_at_end(self, data):
        if self.head == None:
            self.insert_beginning(data)
        
        self.last_node.next_node = Node(data, None)
        self.last_node = self.last_node.next_node

    def to_list(self):
        arr = []
        if self.head == None:
            return arr
        
        node = self.head
        while node:
            arr.append(node.data)
            node = node.next_node
        return arr, 200
    
    def get_user_by_id(self, user_id):
        node = self.head
        while node:         
            if node.data["id"] == int(user_id):
                return node.data
            node = node.next_node #wieso ist das hier der next node???? node bleibt doch einfach immer self.head = node mit dem user.id == 200
        return None
            
