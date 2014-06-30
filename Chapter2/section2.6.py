# These lines that begin with # are comments and will be ignored by Python.

# I use the print function in this code, even though I don't in the book text,
# so that you can run it as a regular script and still get the output. You only
# get output without using print if you're using the interactive window.

#################################  2.6 Classes  ################################


# Import the datetime module and create a new object of the datetime class
import datetime
mydate = datetime.date.today()
print(mydate)

# Use a function that belongs to the class to ask the datetime object what
# day of the week it is
print(mydate.weekday())

# Use another function to return a new date similar to the first one but with
# a different year
newdate = mydate.replace(year=2010)
print(newdate)
print(newdate.weekday())
