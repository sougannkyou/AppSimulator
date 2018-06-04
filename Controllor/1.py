import random

num = '186'
for i in range(8):
    num += str(random.randrange(0, 9))

print(num)
