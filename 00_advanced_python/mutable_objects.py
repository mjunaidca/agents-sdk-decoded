# A mutable object is an object whose state (internal data) can be changed after 
# it's created. Let me explain this concept with clear examples:

# Mutable vs Immutable Objects
# Mutable Objects (Can be changed)

# Lists are mutable
my_list = [1, 2, 3]
print(f"Original: {my_list}")
print(f"Same object? {id(my_list)}")  # Same memory address
my_list.append(4)  # Modifying the same object
print(f"Modified: {my_list}")  # [1, 2, 3, 4]
print(f"Same object? {id(my_list)}")  # Same memory address

# Dictionaries are mutable
my_dict = {"name": "Alice", "age": 25}
print(f"Original: {my_dict}")
print(f"Same object? {id(my_dict)}")  # Same memory address
my_dict["age"] = 26  # Modifying the same object
my_dict["city"] = "NYC"  # Adding new key
print(f"Modified: {my_dict}")  # {'name': 'Alice', 'age': 26, 'city': 'NYC'}
print(f"Same object? {id(my_dict)}")  # Same memory address
# Sets are mutable
my_set = {1, 2, 3}
print(f"Original: {my_set}")
print(f"Same object? {id(my_set)}")  # Same memory address
my_set.add(4)  # Modifying the same object
print(f"Modified set: {my_set}")  # {1, 2, 3, 4}
print(f"Same object? {id(my_set)}")  # Same memory address

print("\n--------------------------------\n")
print("Immutable Objects (Cannot be changed)")  

# Immutable Objects (Cannot be changed)

# Strings are immutable
my_string = "Hello"
print(f"Original: {my_string}")
print(f"Same object? my_string: {id(my_string)}")  # Same memory address
my_string = my_string + " World"  # Creates a NEW object
print(f"Original still: {my_string}")  # "Hello" (unchanged)
print(f"New string: {my_string}")     # "Hello World"
print(f"Same object? new_string: {id(my_string)}")  # Same memory address
print(f"Same object? my_string: {id(my_string)}")  # Same memory address

# Tuples are immutable
my_tuple = (1, 2, 3)
# my_tuple[0] = 5  # This would raise an error!
new_tuple = my_tuple + (4,)  # Creates a NEW tuple
print(f"Original tuple: {my_tuple}")   # (1, 2, 3)
print(f"New tuple: {new_tuple}")       # (1, 2, 3, 4)

# Numbers are immutable
x = 5
print(f"x: {x}")  # x: 5
print(f"Same object? x: {id(x)}")  # Same memory address
y = x
x = 10  # Creates a new integer object
print(f"x: {x}")  # x: 10
print(f"Same object? x: {id(x)}")  # Same memory address
print(f"y: {y}")  # y: 5
print(f"Same object? y: {id(y)}")  # Same memory address

# Numbers are immutable
x = 5
y = x
x = 10  # Creates a new integer object
print(f"x: {x}")  # x: 10
print(f"Same object? x: {id(x)}")  # Same memory address
print(f"y: {y}")  # y: 5
print(f"Same object? y: {id(y)}")  # Same memory address

# Booleans are immutable
x = True
print(f"x: {x}")  # x: True
print(f"Same object? x: {id(x)}")  # Same memory address
y = x

print("\n\n\nExample 3: Why Mutability Matters")
# Immutable approach (creates new objects)
def immutable_approach():
    data = (1, 2, 3)  # Immutable tuple
    # To "change" it, you create a new object
    new_data = data + (4,)
    return new_data  # Original data unchanged

# Mutable approach (modifies existing object)
def mutable_approach():
    data = [1, 2, 3]  # Mutable list
    data.append(4)    # Modifies the same object
    return data       # Same object, but changed

# In agent context, mutability allows:
class AgentContext:
    def __init__(self):
        self.shared_state = {}
    
    def update_state(self, key, value):
        # Multiple tools can modify the same context object
        self.shared_state[key] = value

context = AgentContext()
context.update_state("tool_a_used", True)
context.update_state("tool_b_used", True)

print(context.shared_state)



