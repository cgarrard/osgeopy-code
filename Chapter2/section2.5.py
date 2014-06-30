# These lines that begin with # are comments and will be ignored by Python.

# I use the print function in this code, even though I don't in the book text,
# so that you can run it as a regular script and still get the output. You only
# get output without using print if you're using the interactive window.


#############################  2.5 Flow of control  ############################

#################### If statements

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

#################### While statements

# Print the numbers 0 through 4
n = 0
while n < 5:
    print(n)
    n += 1

#################### For statements

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

#################### Break, continue, and else

# Break out of a loop if i == 5
for i in range(20):
    print(i)
    if i == 5:
        break

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
