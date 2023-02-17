x = [1,2,3,4,5,6,7]
for i in x:
    if i > 3:
        print(i)


keys = ['a','b','c','d','e']
values = [1,2,3,4,5]

dict_a = {i:j for i, j in zip(keys, values) if j > 1}
print(dict_a)