# self vs cls

# Function and method arguments:

# Always use self for the first argument to instance methods.

# Always use cls for the first argument to class methods.

# cls implies that method belongs to the class while self implies
# that the method is related to instance of the class,
# therefore member with cls is accessed by class name
# where as the one with self is accessed by instance of the class...
# it is the same concept as static member and non-static members in java if you are from java background.

# https://stackoverflow.com/questions/4613000/what-is-the-cls-variable-used-for-in-python-classes