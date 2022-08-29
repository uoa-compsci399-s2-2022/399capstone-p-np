def mergesort(array, loc):
    if len(array) == 1:
        return array
    else:
        left = mergesort(array[len(array)//2 + len(array) %2:],loc)
        right = mergesort(array[:len(array)//2],loc)

        new_array = []
        while len(left) > 0 and  len(right) > 0:
            if left[0][loc] > right[0][loc]:
                new_array.append(left[0])
                left.pop(0)
            elif left[0][loc] < right[0][loc]:
                new_array.append(right[0])
                right.pop(0)
            else:
                new_array.append(right[0])
                right.pop(0)

        if len(left) > 0:
            new_array = new_array + left
        else:
            new_array = new_array + right
        return new_array

names = ["aaa 15 55", "sd 65 90", "o 65 90", "i 78 90"]

newlist = []
for x in names:
    x = x.split(" ")
    newlist.append((x[0], int(x[1]), int(x[2])))

newlist = mergesort(newlist, 2)
newlist = mergesort(newlist, 1) 
print(newlist)
                    

        
        
