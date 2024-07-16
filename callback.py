def callbackFunc(s):
    print('Length of the text is : ', s)

def printLength(str, callback):
    def lamdaFunc(d):
        print(d)

    length = len(str)
    lamdaFunc(length)

a = 1 if 0 == 0 and 1 == 2 else 2
if 0 == 0 and 1 == 2:
    a = 1
else:
    a = 2

arr = [x for x in range(10)]
arr = []
for x in range(10):
    arr += [x]

lambda d: print(d)
def func(d):
    print(d)

fSum = lambda a,b: a+b
def sum(a,b):
    return a+b

print(fSum(1,2))
print(sum(1,2))


if __name__ == '__main__':
    printLength("Here Is a String", lambda d: print(d))