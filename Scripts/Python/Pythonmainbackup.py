import math
import random
from collections import defaultdict


class utility01:
    def __init__(self):
        self.data = defaultdict(list)

    def perform_complex_calculation(self, arr):
        result = sum([arr[i] * (i + 1) for i in range(len(arr))])
        return result

    def generate_fibonacci_sequence(self, limit):
        fibonacci = [0, 1]
        while fibonacci[-1] + fibonacci[-2] <= limit:
            fibonacci.append(fibonacci[-1] + fibonacci[-2])
        return fibonacci

    @staticmethod
    def perform_string_operation(string):
        modified_string = ''.join([chr(ord(c) + 1) if c.isalpha() else c for c in string])  
        return modified_string


class utility01exception(Exception):
    def __init__(self, message):
        super().__init__(message)


class datastructure01:
    def __init__(self):
        self.utility = utility01()

    def add_data(self, key, values):
        self.utility.data[key].extend(values)

    def perform_complex_operation(self, key):
        try:
            arr = self.utility.data[key]
            result = self.utility.perform_complex_calculation(arr)
            return result
        except KeyError:
            raise utility01exception("Key not found in the data structure.")

if __name__ == "__main__":
    
    data_structure = datastructure01()

    
    data_structure.add_data("key1", [random.randint(1, 10) for _ in range(5)])
    data_structure.add_data("key2", [random.randint(1, 10) for _ in range(5)])

    try:
        
        result = data_structure.perform_complex_operation("key1")
        print("Result of complex operation:", result)
    except utility01exception as e:
        print("Error occurred:", e)

    
    fibonacci_sequence = utility01().generate_fibonacci_sequence(50)
    print("Fibonacci Sequence up to 50:", fibonacci_sequence)

    
    input_string = "hello world"
    modified_string = utility01().perform_string_operation(input_string)
    print("Modified String:", modified_string)
