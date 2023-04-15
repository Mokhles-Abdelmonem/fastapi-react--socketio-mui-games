def test():
    functions = [test1, test2, test3, test4]
    counter = 0 
    for fun in functions :
        counter += 1
        fun(counter , check=False)

    for i in range(1,2):
        print("counter would be adfsdfsdfsdfd" )
        
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

    list1 = ["R", "N", "B", "Q", "P"]
    list2 = ["S",]
    print(list(set(list1)-set(list2)))

test()