# Name: Behrad Noorani
# Description: This file contains implementation of a hashmap using Open Addressing and its methods using linkedlist
# and dynamic array as its basis. it contains methods for adding, removing and getting values and more.


from include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()

        # capacity must be a prime number
        self._capacity = self._next_prime(capacity)
        for _ in range(self._capacity):
            self._buckets.append(None)

        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def _next_prime(self, capacity: int) -> int:
        """
        Increment from given number to find the closest prime number
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity % 2 == 0:
            capacity += 1

        while not self._is_prime(capacity):
            capacity += 2

        return capacity

    @staticmethod
    def _is_prime(capacity: int) -> bool:
        """
        Determine if given integer is a prime number and return boolean
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        if capacity == 2 or capacity == 3:
            return True

        if capacity == 1 or capacity % 2 == 0:
            return False

        factor = 3
        while factor ** 2 <= capacity:
            if capacity % factor == 0:
                return False
            factor += 2

        return True

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """
        method updates the key / value pair in the hash map. If the given key already exists in
        the hash map its associated value gets replaced with the new value. If the given key is
        not in the hash map, a new key/value pair is added to the appropriate index using quadratic probing.
        if the table load is higher than 0.5 the method resizes the table.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity*2)
        nhash = self._hash_function(key)
        i_index = nhash % self._capacity
        c_index = i_index
        counter = 1
        while self._buckets[c_index] is not None:
            if self._buckets[c_index].is_tombstone is True:
                break
            elif self._buckets[c_index].key == key:
                self._buckets[c_index].value = value
                return
            else:
                c_index = i_index + (counter*counter)
                counter += 1
                if c_index >= self._capacity:
                    c_index = c_index % self._capacity
        self._buckets[c_index] = HashEntry(key, value)
        self._size += 1
        return

    def table_load(self) -> float:
        """
        returns the table load of the hashtable
        """
        load_f = self.get_size() / self.get_capacity()
        return load_f

    def empty_buckets(self) -> int:
        """
        method returns the number of empty buckets in the hashmap
        """
        counter = 0
        for val in range(self.get_capacity()):
            if self._buckets[val] is None:
                counter += 1
        return counter

    def resize_table(self, new_capacity: int) -> None:
        """
        resizes the hashmap table and rehashes the existing values according to the new size/capacity. during that
        precess if the tableload gets higher tan 0.5 again, the table is resized again and the values are rehashed,
        again.
        """
        orig_cap = self.get_capacity()
        if new_capacity < self.get_size():
            return
        if self._is_prime(new_capacity) is False:
            new_capacity = self._next_prime(new_capacity)
        new_arr = DynamicArray()
        curr_size = 0
        for ind in range(new_capacity):
            new_arr.append(None)
        for index in range(orig_cap):
            hash_e = self._buckets[index]
            if hash_e is not None:
                if hash_e.is_tombstone is False:
                    nkey = hash_e.key
                    nval = hash_e.value
                    nhash = self._hash_function(nkey)
                    i_index = nhash % new_capacity
                    c_index = i_index
                    counter = 1
                    while new_arr[c_index] is not None:
                        c_index = i_index + (counter * counter)
                        counter += 1
                        if c_index >= new_capacity:
                            c_index = c_index % new_capacity
                    new_arr.set_at_index(c_index, HashEntry(nkey, nval))
                    curr_size += 1
            if curr_size / new_capacity > 0.5:  # check for tableload being over 0.5
                oldn_capacity = new_capacity
                new_capacity = self._next_prime(new_capacity*2)
                newer_arr = DynamicArray()
                for ind in range(new_capacity):
                    newer_arr.append(None)
                for val in range(oldn_capacity):
                    hash_e2 = new_arr[val]
                    if hash_e2 is not None:
                        nnkey = hash_e2.key
                        nnval = hash_e2.value
                        nhash2 = self._hash_function(nnkey)
                        ii_index = nhash2 % new_capacity
                        cc_index = ii_index
                        ccounter = 1
                        while newer_arr[cc_index] is not None:
                            cc_index = ii_index + (ccounter * ccounter)
                            ccounter += 1
                            if cc_index >= new_capacity:
                                cc_index = cc_index % new_capacity
                        newer_arr.set_at_index(cc_index, HashEntry(nnkey, nnval))
                new_arr = newer_arr
        self._buckets = new_arr
        self._capacity = new_capacity
        return

    def get(self, key: str) -> object:
        """
        returns the value of the given key if it exits, if it doesn't returns none.
        """
        nhash = self._hash_function(key)
        i_index = nhash % self.get_capacity()
        c_index = i_index
        start_from_first = False
        counter = 1
        while self._buckets[c_index] is not None:
            if self._buckets[c_index].key != key:
                c_index = i_index + (counter * counter)
                counter += 1
                if c_index >= self._capacity:
                    c_index = c_index % self._capacity
                    start_from_first = True
                if start_from_first is True and c_index > i_index:
                    return None
            elif self._buckets[c_index].key == key and self._buckets[c_index].is_tombstone is False:
                break
            else:
                c_index = i_index + (counter * counter)
                counter += 1
                if c_index >= self._capacity:
                    c_index = c_index % self._capacity
                    start_from_first = True
                if start_from_first is True and c_index > i_index:
                    return None
        if self._buckets[c_index] is None:
            return None
        return self._buckets[c_index].value

    def contains_key(self, key: str) -> bool:
        """
        returns True if the given key is in the hashmap and false if not.
        """
        if self._size == 0:
            return False
        else:
            nhash = self._hash_function(key)
            i_index = nhash % self.get_capacity()
            c_index = i_index
            start_from_first = False
            counter = 1
            while self._buckets[c_index] is not None:
                if self._buckets[c_index].key != key:
                    c_index = i_index + (counter * counter)
                    counter += 1
                    if c_index >= self._capacity:
                        c_index = c_index % self._capacity
                        start_from_first = True
                    if start_from_first is True and c_index > i_index:
                        return False
                elif self._buckets[c_index].key == key and self._buckets[c_index].is_tombstone is False:
                    break
                else:
                    c_index = i_index + (counter * counter)
                    counter += 1
                    if c_index >= self._capacity:
                        c_index = c_index % self._capacity
                        start_from_first = True
                    if start_from_first is True and c_index > i_index:
                        return False
            if self._buckets[c_index] is None:
                return False
            return True

    def get_key_index(self, key: str):
        """
        returns the index # of the given key
        """
        if self._size == 0:
            return False
        else:
            nhash = self._hash_function(key)
            i_index = nhash % self.get_capacity()
            c_index = i_index
            start_from_first = False
            counter = 1
            while self._buckets[c_index] is not None:
                if self._buckets[c_index].key != key:
                    c_index = i_index + (counter * counter)
                    counter += 1
                    if c_index >= self._capacity:
                        c_index = c_index % self._capacity
                        start_from_first = True
                    if start_from_first is True and c_index > i_index:
                        return False
                elif self._buckets[c_index].key == key and self._buckets[c_index].is_tombstone is False:
                    break
            if self._buckets[c_index] is None:
                return False
            return c_index

    def remove(self, key: str) -> None:
        """
        removes the given key from the table by setting its tombstone flag to True
        """
        if self._size == 0:
            return
        if self.contains_key(key) is True:
            index = self.get_key_index(key)
            self._buckets[index].is_tombstone = True
            self._size -= 1
            return
        else:
            return

    def clear(self) -> None:
        """
        clears the hash table of all entries and resets size to 0
        """
        self._buckets = DynamicArray()
        for _ in range(self._capacity):
            self._buckets.append(None)
        self._size = 0

    def get_keys_and_values(self) -> DynamicArray:
        """
        returns a DA filled with tuples of each key and value in the hashmap
        """
        ret_arr = DynamicArray()
        for index in range(self._capacity):
            if self._buckets[index] is not None:
                if self._buckets[index].is_tombstone is False:
                    tup = (self._buckets[index].key, self._buckets[index].value)
                    ret_arr.append(tup)
        return ret_arr

    def get_buckets(self):
        """
        method that returns the DA buckets of the hashmap, used for accessing the buckets
        """
        return self._buckets


# ------------------- BASIC TESTING ---------------------------------------- #
if __name__ == "__main__":
    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(53, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())

    # print("\nPDF - put example 2")
    # print("-------------------")
    # m = HashMap(41, hash_function_2)
    # for i in range(50):
    #     m.put('str' + str(i // 3), i * 100)
    #     if i % 10 == 9:
    #         print(m.empty_buckets(), round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - table_load example 1")
    # print("--------------------------")
    # m = HashMap(101, hash_function_1)
    # print(round(m.table_load(), 2))
    # m.put('key1', 10)
    # print(round(m.table_load(), 2))
    # m.put('key2', 20)
    # print(round(m.table_load(), 2))
    # m.put('key1', 30)
    # print(round(m.table_load(), 2))
    #
    # print("\nPDF - table_load example 2")
    # print("--------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(50):
    #     m.put('key' + str(i), i * 100)
    #     if i % 10 == 0:
    #         print(round(m.table_load(), 2), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 1")
    # print("-----------------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key1', 30)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    # m.put('key4', 40)
    # print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - empty_buckets example 2")
    # print("-----------------------------")
    # m = HashMap(53, hash_function_1)
    # for i in range(150):
    #     m.put('key' + str(i), i * 100)
    #     if i % 30 == 0:
    #         print(m.empty_buckets(), m.get_size(), m.get_capacity())
    #
    # print("\nPDF - resize example 1")
    # print("----------------------")
    # m = HashMap(23, hash_function_1)
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    # m.resize_table(30)
    # print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    #
    # print("\nPDF - resize example 2")
    # print("----------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 13)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    #
    # for capacity in range(111, 1000, 117):
    #     m.resize_table(capacity)
    #
    #     if m.table_load() > 0.5:
    #         print(f"Check that the load factor is acceptable after the call to resize_table().\n"
    #               f"Your load factor is {round(m.table_load(), 2)} and should be less than or equal to 0.5")
    #
    #     m.put('some key', 'some value')
    #     result = m.contains_key('some key')
    #     m.remove('some key')
    #
    #     for key in keys:
    #         # all inserted keys must be present
    #         result &= m.contains_key(str(key))
    #         # NOT inserted keys must be absent
    #         result &= not m.contains_key(str(key + 1))
    #     print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    # print("\nPDF - get example 1")
    # print("-------------------")
    # m = HashMap(31, hash_function_1)
    # print(m.get('key'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    #
    # print("\nPDF - get example 2")
    # print("-------------------")
    # m = HashMap(151, hash_function_2)
    # for i in range(200, 300, 7):
    #     m.put(str(i), i * 10)
    # print(m.get_size(), m.get_capacity())
    # for i in range(200, 300, 21):
    #     print(i, m.get(str(i)), m.get(str(i)) == i * 10)
    #     print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)
    #
    # print("\nPDF - contains_key example 1")
    # print("----------------------------")
    # m = HashMap(11, hash_function_1)
    # print(m.contains_key('key1'))
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key3', 30)
    # print(m.contains_key('key1'))
    # print(m.contains_key('key4'))
    # print(m.contains_key('key2'))
    # print(m.contains_key('key3'))
    # m.remove('key3')
    # print(m.contains_key('key3'))
    #
    # print("\nPDF - contains_key example 2")
    # print("----------------------------")
    # m = HashMap(79, hash_function_2)
    # keys = [i for i in range(1, 1000, 20)]
    # for key in keys:
    #     m.put(str(key), key * 42)
    # print(m.get_size(), m.get_capacity())
    # result = True
    # for key in keys:
    #     # all inserted keys must be present
    #     result &= m.contains_key(str(key))
    #     # NOT inserted keys must be absent
    #     result &= not m.contains_key(str(key + 1))
    # print(result)
    #
    # print("\nPDF - remove example 1")
    # print("----------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get('key1'))
    # m.put('key1', 10)
    # print(m.get('key1'))
    # m.remove('key1')
    # print(m.get('key1'))
    # m.remove('key4')
    #
    # print("\nPDF - clear example 1")
    # print("---------------------")
    # m = HashMap(101, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # m.put('key2', 20)
    # m.put('key1', 30)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - clear example 2")
    # print("---------------------")
    # m = HashMap(53, hash_function_1)
    # print(m.get_size(), m.get_capacity())
    # m.put('key1', 10)
    # print(m.get_size(), m.get_capacity())
    # m.put('key2', 20)
    # print(m.get_size(), m.get_capacity())
    # m.resize_table(100)
    # print(m.get_size(), m.get_capacity())
    # m.clear()
    # print(m.get_size(), m.get_capacity())
    #
    # print("\nPDF - get_keys_and_values example 1")
    # print("------------------------")
    # m = HashMap(11, hash_function_2)
    # for i in range(1, 6):
    #     m.put(str(i), str(i * 10))
    # print(m.get_keys_and_values())
    #
    # m.resize_table(2)
    # print(m.get_keys_and_values())
    #
    # m.put('20', '200')
    # m.remove('1')
    # m.resize_table(12)
    # print(m.get_keys_and_values())
