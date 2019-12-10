
def hello_world():
    return "Hello, World!"


def sum_without_dups(l):
    already_found = []
    sum = 0 
    for item in l:
        if item in already_found:
            continue
        else:
            already_found.append(item)
            sum += item
    return sum

def palindrome(x):
    x = str(x)
    for i in range(0, (len(x) + 1)//2):
        if not x[i] == x[-1-i]:
            return False
    return True

def sum_multiples(num):
    sum  = 0
    for i in range(0, num):
        if i % 7 == 0 or i % 3 == 0:
            sum += i
    return sum

def num_func_mapper(nums, funs):
    finals = []
    for fun in funs:
        finals.append(fun(nums))
    return finals

def pythagorean_triples(n):
    triples = []
    for i in range(1, n):
        for j in range(i,n):
            for k in range(j,n):
                if i**2 + j**2 == k**2:
                    triples.append((i,j,k))
    triples.sort(key=max)
    return triples