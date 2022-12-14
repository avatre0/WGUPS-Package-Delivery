# Hash Map

class HashMap:
    # Constructor
    # Has default size of 32, but can create any size
    # O(n)
    def __init__(self, init_cap=32):
        self.size = init_cap
        self.map = [None] * self.size

    # Hashes the key
    # O(n)
    def _get_hash(self, key):
        hash = 0
        for char in str(key):
            hash += ord(char)
        return hash % self.size

    # Adds Key/Value pare to the hash map
    # also updates the value if it has the same keys
    # O(n)
    def add(self, key, value):
        key_hash = self._get_hash(key)
        key_value = [key, value]

        # If the key is not in the map just add the key/value pair
        if self.map[key_hash] is None:
            self.map[key_hash] = list([key_value])
            return True
        else:
            # If he Key is already in the map loop through bucket
            for pair in self.map[key_hash]:
                if pair[0] == key: # If the Key is the same
                    pair[1] = value # Overwrite the value
                    return True
            self.map[key_hash].append(key_value) # No same key is found add a new value to the bucket
            return True

    # Return the Value of a key if found
    # Returns nothing if key is not found
    # O(n)
    def get(self, key):
        key_hash = self._get_hash(key)
        if self.map[key_hash] is not None:
            for pair in self.map[key_hash]:
                if pair[0] == key:
                    return pair[1]
        return None

    # Removes key/value from map if found
    # Returns false if not found
    # O(n)
    def delete(self, key):
        key_hash = self._get_hash(key)

        if self.map[key_hash] is None:
            return False
        for i in range(0, len(self.map[key_hash])):
            if self.map[key_hash][i][0] == key:
                self.map[key_hash].pop(i)
                return True
        return False

    # Returns an array of keys in the hashmap
    # O(n)
    def keys(self):
        arr = []
        for i in range(0, len(self.map)):
            if self.map[i]:
                arr.append(self.map[i][0])
        return arr

    # Print All items in hash map
    # O(n^2)
    def return_all_items(self):
        item_list = []
        for item in self.map:
            if item is not None:
                for key_item_pair in item:
                    item_list.append(key_item_pair[1])

        return item_list