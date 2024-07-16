# print('hello world!')

# hello i'm Huy

# System.out.println("hello i'm Huy");
# print("hello i'm Huy")
# int float string boolean

# arr = [1, 'O', 3, 4, 5]                         arr => p{p1, p2, p3,p4, p5}
# arr2 = [9, 8, 7]                                arr2 => pp{p9,p8,p7}
# arr.append(arr2)                                arr => p{p1, p2, p3,p4, p5, pp}
# arr2[1] = 10                                    arr2 => pp{p9,p10,p7}
# arr2                                            pp{p9,p10,p7}
# arr                                             p{p1, p2, p3,p4, p5, pp}
# t = (1,3,4,6)

# d = {
#     "key1": "value1",
#     "key2": 2,
#     "key3": True,
#     "key4": {
#         "child1": "",
#         "child2": "",
#         "child3": {
#             "childOfchild": ""
#         }
#     }
# }
# for key in d.keys():
#     if d[key] == 2:
#         print("Key can tim la ", key)
#         break

# +,-,*,/, **, %, //
# ==, !=, >, <, >=, <=,
# not(!), and(&), or (|)
# 
# a = 2

# str = "chan" if a%2 == 0 else "le"

# arr = [1,2,3,4,5,6,7,8,9,0]
# newArr = ["le", "chan", "le",...,"chan"]
# newArr = ["chan" if x %2 == 0 else "le" for x in arr]
# print(newArr)
# for item in arr:
#     if item%2 == 0:
#         newArr = newArr + [item]
#         print(newArr)

# def sum(a:int, b:float) -> int:
#     return a + b

# def minus(a,b):
#     return a-b

# def bigFunction():
#     def child():
#         return "child"
#     return child() + " from bigFunction"

# de quy
# N! = 

# def frac(n:int):
#     return 1 if n == 0 else n*frac(n-1)

# print(frac(3))

"""
F(0) = 1
F(1) = 1
F(N) = F(N-1) + F(N-2)
"""

# def fiboRec(n):
#     return 1 if n == 0 or n == 1 else fiboRec(n-1) + fiboRec(n-2)

# def fiboLoop(n):
#     arr = []
#     for i in range(n+1):
#         if i == 0 or i == 1:
#             arr.append(1)
#         else:
#             arr.append(arr[i-1] + arr[i-2])
#         # print(arr)
#     return arr[n]
# N = 3
# print(fiboRec(5))
# print(fiboLoop(5))

# O(n) < O(n^2) < O(n^n)

# class A:
#     # attribute
#     # constructor
#     # method
#     att1 = 1
#     att2 = "2"
#     att3 = True
#     # self => this java

#     def __init__(self) -> None:
#         self.att1=""

#     def __init__(self, a,b,c) -> None:
#         self.att1=a
#         self.att2=b
#         self.att4=c

#     def func(self):
#         return self.att1 + self.att4
#     def func(self,a):
#         return self.att1 + self.att4 + a

# a = A(1, "2", 4)
# print(a.func(2))

# class B(A):
#     def __init__(self, a, b, c) -> None:
#         super().__init__(a, b, c)
# b = B("1", 2, True)
# print(b.att1)


# class A:
#     def func():
#         return "From A"

# class B(A):
#     pass
#     # def func():
#     #     return "From B"

# class C(A):
#     def func():
#         return "From C"

# class D(B,C):
#     pass

