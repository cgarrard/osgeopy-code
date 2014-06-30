# These lines that begin with # are comments and will be ignored by Python.

# I use the print function in this code, even though I don't in the book text,
# so that you can run it as a regular script and still get the output. You only
# get output without using print if you're using the interactive window.


######################  2.2 Basic structure of a script  ######################

# Import the random module and use it to get a random number
import random
print(random.gauss(0, 1))


###############################  2.3 Variables  ###############################

# Creating a variable
n = 10
print(n)

# Changing n from integer to string
n = 'Hello world'
print(n)

# Attempt to add a string (n) and integer together
msg = n + 1

# Test for equality
n = 10
print(n == 10)
print(n == 15)
