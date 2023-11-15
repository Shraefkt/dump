'''
CJG: Some things to note:
1)  Call your functions via a "main" function (the "if __name__ == '__main__'" below). This is useful if you want to import your functions into another source file in the future but do not want to invoke your example code.
2)  As code gets more complex, variables will need to be named more descriptively. Variable names should indicate the purpose of the existence as much as possible.
3)  Name functions descriptively. Like variable names, function names should indicate the purpose of the existence as much as possible.
4)  Comments can be useful for describing what a function does / why a function does what it does, but remember to keep them up to date with the functionality. Also, if you name your functions descriptively, you will not need excessive comments!
5)  As Python lacks explicit type information (int, float, list of ints, etc.) in general, it may be useful to indicate variables' types using comments somewhere).
6)  Avoid global variables as much as possible, unless you know what you are doing / they are meant to be constants.
7)  Take a look at https://peps.python.org/pep-0008 for style guides that you can try to adopt.
'''

'''
    Calculate minimal cover of ranged query [a, b].

    Input:
        a, b: ints
    Output:
        list of ints for minimal cover
'''
def calc_min_cover(a, b):
    # base cases
    if a == b:
        return [a]
    if b - a == 1 and a % 2 == 1:
        return [a, b]

    # recursive case
    min_cover = []
    if a % 2 == 1:
        min_cover.append(a)
    min_cover += calc_min_cover((a+1) // 2, (b-1) // 2) # recursive call for solving smaller problem
    if b % 2 == 0:
        min_cover.append(b)
    return min_cover

if __name__ == '__main__':
    a = int(input("Input lower limit "))
    b = int(input("Input upper limit "))
    assert 0 < a <= b and len(bin(a)) == len(bin(b)), 'a and b are not on the same layer of a binary tree!'

    print(calc_min_cover(a, b))
