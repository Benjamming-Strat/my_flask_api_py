class Node:
    def __init__(self, data=None, next_node=None):
        self.data = data
        self.next_node = next_node



class Data:
    def __init__(self, key, value):
        self.key = key
        self.value = value

class Hashtable:
    def __init__(self, table_size):
        self.table_size = table_size
        self.hash_table = table_size * [None]

    def custom_hash(self, key):
        hash_value = 0
        for i in key:
            hash_value += ord(i) #transform a character to its hashvalue e.g A=65
            hash_value = (hash_value * ord(i)) % self.table_size #reduce the possibilty to have 2 same values, make it unique so to say
            return hash_value

    def add_key_value(self, key, value):
        # this hashtable will probably lead into a collision becasue we will have the same hash_value for different keys
        # for the purpose of studying linkedlists this will be ok so far
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] == None:
            self.hash_table[hashed_key] = Node(Data(key,value),None)
        else:
            # takes the value of the index from hashed key
            # loops thorugh all nodes until the end and "appends" the last node to the index in the hash_table
            node = self.hash_table[hashed_key]
            while node.next_node:
                node= node.next_node
            
            node.next_node = Node(Data(key,value), None)
        
    def get_value(self, key):
        hashed_key = self.custom_hash(key)
        if self.hash_table[hashed_key] != None:
            node = self.hash_table[hashed_key]
            if node.next_node == None:
                #if its a single node only
                return node.data.value
            while node.next_node:
                # data is attribute, consists of class Data(key, value)
                if key == node.data.key:
                    return node.data.value
                else:
                    node = node.next_node
                if key == node.data.key:
                    return node.data.value
                else: #key does not exist
                    return None
    

            