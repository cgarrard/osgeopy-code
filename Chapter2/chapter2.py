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


###############################  2.4 Data types  ##############################

#################### 2.4.1 Booleans

print(True or False)
print(not False)
print(True and False)
print(True and not False)

#################### 2.4.2 Numeric types

print(27 / 7) # Integer (Python 2.7) or floating point (Python 3) math
print(27.0 / 7.0) # Floating point math in both
print(27 / 7.0) # Floating point math in both

print(27 / 7) # Integer (Python 2.7) or floating point (Python 3) math
print(27 // 7) # Force integer point math in Python 3

# Convert between integer and float
print(float(27))
print(int(27.9))

print(round(27.9))

#################### 2.4.3 Strings

s = 'Hello world'
print(s)

# String that contains quotes
sql = "SELECT * FROM cities WHERE country = 'Canada'"
print(sql)

# Does not work because the first single quote ends the string
print('Don't panic!')

# This one works because the backslash tells Python to include it in the string
print('Don\'t panic!')

# Join two strings
s = 'Beam me up ' + 'Scotty'
print(s)

# Formatting strings using indexes in the placeholders
print('I wish I were as smart as {0} {1}'.format('Albert', 'Einstein'))
print('I wish I were as smart as {1}, {0}'.format('Albert', 'Einstein'))

# Escape characters (\t means tab, \n means newline)
print('Title:\tMoby Dick\nAuthor:\tHerman Melville')

#################### Windows filenames

# Import the os module for the next couple of Windows examples
import os

# Backslashes in Windows filenames
# Change the path to a file that exists on your Windows machine so that there
# is a \t in the path (so a temp folder is good)
print(os.path.exists('d:\temp\cities.csv'))

# To see what Python thinks you're saying
print('d:\temp\cities.csv')

# Three ways to fix the problem
print(os.path.exists('d:/temp/cities.csv')) # Use forward slashes instead
print(os.path.exists('d:\\temp\\cities.csv')) # Use double-backslashes
print(os.path.exists(r'd:\temp\cities.csv')) # Prefix the string with r

#################### 2.4.4 Lists and tuples

# Create a list
data = [5, 'Bob', 'yellow', -43, 'cat']
print(data)

# Get stuff out of it by index
print(data[0])
print(data[2])
print(data[-1])
print(data[-3])

# Get sublists
print(data[1:3])
print(data[-4:-1])

# Change list values
data[2] = 'red'
print(data)
data[0:2] = [2, 'Mary']
print(data)

# Append and delete values
data.append('dog')
print(data)
del data[1]
print(data)

# Get the length of a list
print(len(data))

# Find out if values are in a list
print(2 in data)
print('Mary' in data)

# Create a tuple and get values out of ities
data = (5, 'Bob', 'yellow', -43, 'cat')
print(data)
print(data[2])
print(data[-3])
print(data[1:3])

# Get the length of a tuple and check if it contains a value
print(len(data))
print('Bob' in data)

# Try, and fail, to change a value of a tuple
data[0] = 10

#######################  Error messages are your friend  #######################

# This will cause an error because you cannot change the value of a tuple
data = (5, 'Bob', 'yellow', -43, 'cat')
data[0] = 10

# Function that the next two examples use. It takes two values as parameters
# and returns their sum.
def add(n1, n2):
  return n1 + n2

# This one will work
x = add(3, 5)
print(x)

# This one fails because '1' is a string, which cannot be added to a number (x)
y = add(x, '1')
print(y)

#################### 2.4.5 Sets

# Create a set
data = set(['book', 6, 13, 13, 'movie'])
print(data)

# Add stuff to the set; 'movie' will not be added again
data.add('movie')
data.add('game')
print(data)

# Check if a value is in the set
print(13 in data)

# Create another set and union and intersect it with the first set
info = set(['6', 6, 'game', 42])
print(data.union(info)) # All values from both sets
print(data.intersection(info)) # Only values contained in both

#################### 2.4.6 Dictionaries

# Create a dictionary and get values out of it
data = {'color': 'red', 'lucky number': 42, 1: 'one'}
print(data)
print(data[1])
print(data['lucky number'])

# Add a value
data[5] = 'candy'
print(data)

# Change a value
data['color'] = 'green'
print(data)

# Delete a value
del data[1]
print(data)

# Check if a key is in the dictionary
print('color' in data)


#############################  2.5 Flow of control  ############################

#################### 2.5.1 If statements

# Print a different message depending on the value of n. Try changing the value
# of n.
n = 1
if n == 1:
    print('n equals 1')
else:
    print('n does not equal 1')
print('This is not part of the condition')

# Test multiple conditions. Try changing the value of n.
n = 0
if n == 1:
    print('n equals 1')
elif n == 3:
    print('n does not equal 3')
elif n > 5:
    print('n is greater than 5')
else:
    print('what is n?')

# Blank strings resolve to False
if '':
    print('a blank string acts like True')
else:
    print('a blank string acts like false')

# Empty lists also resolve to false, while lists with stuff in them do not
if [1]:
    print('a non-empty list acts like True')
else:
    print('a non-empty list acts like False')

#################### 2.5.2 While statements

# Print the numbers 0 through 4
n = 0
while n < 5:
    print(n)
    n += 1

#################### 2.5.3 For statements

# Print a message for each name in the list
names = ['Chris', 'Janet', 'Tami']
for name in names:
    print('Hello {}!'.format(name))

# Use range() to increment n 20 times
n = 0
for i in range(20):
    n += 1
print(n)

# Use range() to compute the factorial of 20
n = 1
for i in range(1, 21):
    n = n * i
print(n)

#################### 2.5.4 Break, continue, and else

# Break out of a loop if i == 3
for i in range(5):
    if i == 3:
        break
    print(i)

# Go back to the beginning of the loop and skip the print function if i == 3
for i in range(5):
    if i == 3:
        continue
    print(i)

# Use a break statement to get out of the loop if we find the number 2...
for i in [0, 5, 7, 2, 3]:
    if i == 2:
        print('Found it!')
        break
else:
    print('Could not find 2')

# ...but use an else clause to say we couldn't find it if it's not there
for i in [0, 5, 7, 3]:
    if i == 2:
        print('Found it!')
        break
else:
    print('Could not find 2')


################################  2.6 Functions  ###############################

# Write a function to calculate factorials
def factorial(n):
    answer = 1
    for i in range(1, n + 1):
        answer = answer * i
    return answer

# Use the function like this:
fact5 = factorial(5)
print(fact5)


# Change the function so it will optionally print the answer
def factorial(n, print_it=False):
    answer = 1
    for i in range(1, n + 1):
        answer = answer * i
    if print_it:
        print('{0}! = {1}'.format(n, answer))
    return answer

# Use the function without printing the answer
fact5 = factorial(5)

# Use the function and have it print the answer
fact5 = factorial(5, True)

# Use the function from a module
import myfuncs
fact5 = myfuncs.factorial(5)
print(fact5)


#################################  2.7 Classes  ################################

# Import the datetime module and create a new object of the datetime class
import datetime
datetype = datetime.date
mydate = datetype.today()
print(mydate)

# Use a function that belongs to the class to ask the datetime object what
# day of the week it is
print(mydate.weekday())

# Use another function to return a new date similar to the first one but with
# a different year
newdate = mydate.replace(year=2010)
print(newdate)
print(newdate.weekday())
