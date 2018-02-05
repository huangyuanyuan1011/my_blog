from django.test import TestCase

# Create your tests here.


import time,os,random


#
# print(set((2,3,4,5))-set((1,2,3,4)))
# print(set((1,2,3,4))-set((2,3,4,5)))

str = "12345678qwertyuioasdfghj"
str1 = ''.join(random.choice(str) for i in range(7))
print(str1)