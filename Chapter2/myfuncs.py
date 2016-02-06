def factorial(n, print_it=False):
    """Retuns the factorial of n, optionally printing it first."""
    answer = 1
    for i in range(1, n + 1):
        answer = answer * i
    if print_it:
        print('{0}! = {1}'.format(n, answer))
    return answer
