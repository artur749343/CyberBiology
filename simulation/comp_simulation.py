import pygame
import numpy as np
pygame.init()

def end(new_arr,arr,x,y,gen,x1,y1):
    return gen+MAX_GEN

def inc(new_arr,arr,x,y,gen,x1,y1):
    if arr[x+x1,y1+y,0]==2:
        new_arr[x,y,gen+1]+=1
    return gen+2

def p(new_arr,arr,x,y,gen,x1,y1):
    print(arr[x,y])
    return gen+2
# info = pygame.display.Info()
# width, height=info.current_w-10,info.current_h-50
width, height=1000,1000
surface = pygame.display.set_mode((width,height), pygame.RESIZABLE)
SIZE=20
MAX_GEN=4
W,H=width//SIZE,height//SIZE
arr=np.zeros((W, H,MAX_GEN+1), dtype=np.int8)
new_arr=arr.copy()
clock = pygame.time.Clock()

gens=[
    end,
    inc,
    p
]


def update(new_arr, arr, x, y):
    for x1 in range(-1,2):
        for y1 in range(-1,2):
            if not (x1==0 and y1==0):
                if 2==arr[x,y,0]:
                    if 1==arr[x1+x,y1+y,0]:
                        new_arr[x1+x,y1+y,0]=2
                        new_arr[x,y,0]=3
                    else:
                        new_arr[x,y,0]=3
                elif 3==arr[x,y,0]:
                    new_arr[x,y,0]=1
    if 4==arr[x,y,0]:
        if arr[x-1,y,0]==2:
            new_arr[x,y,arr[x,y,1]]=arr[x,y,arr[x,y,1]]+1
        elif arr[x+1,y,0]==2:
            new_arr[x,y,arr[x,y,1]]=arr[x,y,arr[x,y,1]]-1
        elif arr[x,y-1,0]==2 and arr[x,y,1]<MAX_GEN:
            new_arr[x,y,1]=arr[x,y,1]+1
        elif arr[x,y+1,0]==2 and 2<arr[x,y,1]:
            new_arr[x,y,1]=arr[x,y,1]-1
        gen=2
        print(arr[x,y], "t")
        while gen<MAX_GEN:
            gen=gens[arr[x,y,gen]](new_arr,arr,x,y,gen,x1,y1)

time_go=True
time=0
while True:
    surface.fill((0,0,0))


    mouse = pygame.mouse.get_pos()
    keys=pygame.key.get_pressed()
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT:
            pygame.quit()
        elif keys[pygame.K_0]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE,0]=0
        elif keys[pygame.K_1]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE,0]=1
        elif keys[pygame.K_2]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE,0]=2
        elif keys[pygame.K_3]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE,0]=3
        elif keys[pygame.K_4]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE]=[4,2,0,0,0]
        elif keys[pygame.K_SPACE]:
            time_go=not time_go

    for x in range(W):
        for y in range(H):
            if arr[x,y,0]==1:
                pygame.draw.rect(surface, (255,0,0), (x*SIZE,y*SIZE,SIZE,SIZE))
            elif arr[x,y,0]==2:
                pygame.draw.rect(surface, (0,255,0), (x*SIZE,y*SIZE,SIZE,SIZE))
            elif arr[x,y,0]==3:
                pygame.draw.rect(surface, (0,0,255), (x*SIZE,y*SIZE,SIZE,SIZE))
            elif arr[x,y,0]==4:
                pygame.draw.rect(surface, (0,255,255), (x*SIZE,y*SIZE,SIZE,SIZE))
            if time_go and time%10==0:
                update(new_arr, arr, x, y)
    time+=1
    arr=new_arr.copy()
    pygame.display.update()
    clock.tick(60)