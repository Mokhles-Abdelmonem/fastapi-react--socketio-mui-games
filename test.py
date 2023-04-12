def test():
    functions = [test1, test2, test3, test4]
    counter = 0 
    for fun in functions :
        counter += 1
        fun(counter , check=False)


        
def test1(counter, check=False):
    print("Test number")
    print(counter)
    if check :
        print("Check is True")

        
def test2(counter, check=False):
    print("Test number")
    print(counter)
    if check :
        print("Check is True")

        
def test3(counter, check=False):
    print("Test number")
    print(counter)
    if check :
        print("Check is True")

        
def test4(counter, check=False):
    print("Test number")
    print(counter)
    if check :
        print("Check is True")
    i = -1
    print("the number", 1+i)
    list_set = [(1, 4), (1, 3)]
    if [1, 4] in list_set:
        print("the number in the list")
    lists = ["R", "N", "B", "Q", "P"]
    lists.remove("r")
    print(lists)

test()