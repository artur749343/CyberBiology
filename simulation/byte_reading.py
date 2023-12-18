import numpy as np
import pygame

def write_data(path:str, data, size):
    
    with open(path, "rb") as f:
        byte=bytes(size) if 0==len(f.read()) else bytes()


    for x in range(size[0]):
        for y in range(size[1]):
            byte+=bytes(data[x,y])

    with open(path, "ab") as f:
        f.write(byte)


def read(path):
    with open(path, "rb") as f:
        byte=f.read()
        time_line=int((len(byte)-4)/byte[0]/byte[1]/(byte[2]+byte[3]))
        arr = np.zeros((time_line, byte[0], byte[1], byte[2]+byte[3]), dtype=np.int8)
        i=4
        for t in range(time_line):
            for x in range(byte[0]):
                for y in range(byte[1]):
                    for z in range(byte[2]+byte[3]):
                        arr[t,x,y,z]=byte[i] if byte[i]<128 else byte[i]-256
                        i+=1
    return arr, byte[0:4]

def clear(path):
    with open(path, "wb") as f:
        f.write(bytes())