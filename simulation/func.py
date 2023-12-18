import random

def mutation():
    res=random.randint(0,3)
    if res<2:
        return 0
    elif res==2:
        res=-1
        while random.randint(0,1) and -10<res:
            res-=1
        return res
    elif res==3:
        res=1
        while random.randint(0,1) and res<10:
            res+=1
        return res

def f(size, arr, new_arr, x, y, g):
    if g<size[2]:
        res=[(x+(arr[x,y,g+n]%3)-1,y+(arr[x,y,g+n]//3%3)-1) for n in range(1,3)]
    else:
        return g+3
    for x2, y2 in res:
        if 0<x2<size[0] and 0<y2<size[1] and arr[x2,y2,0]==0 and new_arr[x2,y2,0]==0:
            new_arr[x2,y2]=arr[x,y]
            new_arr[x2,y2,random.randint(size[3], size[2]+size[3]-1)]+=mutation()
    return g+3

def end(size, arr, new_arr, x, y, g):
    return g+size[2]


gens={
    0: end,
    1: f
}


def Gen(size, arr, new_arr, x, y):
    g=size[3]
    while g<size[2]+size[3]:
        if arr[x,y,g] in gens:
            g=gens[arr[x,y,g]](size, arr, new_arr, x, y, g)
        else:
            g+=1

# x,y=0,0

# n=[254//(4**(3-x))%4 for x in range(4)]
# for n1 in n:
#     x1,y1=[(x,y+1), (x+1,y), (x,y-1), (x-1,y)][n1]
# print(x1,y1)