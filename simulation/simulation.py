import pygame, byte_reading, func
import numpy as np

pygame.init()

def game():
    WIDTH, HEIGHT = 1000, 1000
    SIZE=20
    GEN_SIZE=4
    CEIL_DATA=2
    W,H=WIDTH//SIZE,HEIGHT//SIZE
    surface = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    time=0
    arr = np.zeros((W, H, GEN_SIZE+CEIL_DATA), dtype=np.int8)
    new_arr=arr.copy()
    byte_reading.clear("data.sm")

    while True:
        surface.fill(pygame.Color('black'))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        
        keys=pygame.key.get_pressed()
        if keys[pygame.K_1]:
            mx,my=pygame.mouse.get_pos()
            new_arr[mx//SIZE, my//SIZE,0:5]=[3,0,1,5,0]
        font = pygame.font.SysFont(None, 24)
        img = font.render(str(time), True, (255,255,255))
        surface.blit(img, (20, 20))
        img = font.render(str(int(clock.get_fps())), True, (255,255,255))
        surface.blit(img, (20, 50))

        for x in range(W):
            for y in range(H):
                if arr[x,y,0]==1:
                    pygame.draw.rect(surface, (255,0,0), (x*SIZE,y*SIZE,SIZE,SIZE))
                elif arr[x,y,0]==2:
                    pygame.draw.rect(surface, (0,255,0), (x*SIZE,y*SIZE,SIZE,SIZE))
                elif arr[x,y,0]==3:
                    pygame.draw.rect(surface, (0,0,255), (x*SIZE,y*SIZE,SIZE,SIZE))
                
                if arr[x,y,1]>4:
                    new_arr[x,y]=[0]*(GEN_SIZE+CEIL_DATA)
                if arr[x,y,0]!=0:
                    new_arr[x,y,1]=arr[x,y,1]+1
                    func.Gen([W,H,GEN_SIZE,CEIL_DATA], arr, new_arr, x, y)
        arr=new_arr.copy()
        byte_reading.write_data("data.sm", arr, [W,H,GEN_SIZE,CEIL_DATA])

        pygame.display.flip()
        clock.tick(60)
        time+=1



def vising_mode(surface, WIDTH, HEIGHT):
    arr, size=byte_reading.read("data.sm")
    W,H=size[0:2]
    info = pygame.display.Info()
    S_WIDTH,S_HEIGHT=1000,1000
    SIZE=int(S_WIDTH/W)
    FPS=60
    clock, time =pygame.time.Clock(), 0
    button=pygame.Rect(WIDTH/2-50,HEIGHT-75,100,50)
    active_scroll=False
    time_speed=10
    while True:
        surface.fill(pygame.Color('black'))

        mouse = pygame.mouse.get_pos()
        fps=int(clock.get_fps())
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if button.collidepoint(mouse):
                    active_scroll=True
                else:
                    active_scroll=False
            if event.type==pygame.MOUSEBUTTONUP:
                active_scroll=False
            if event.type == pygame.MOUSEMOTION:
                if active_scroll:
                    if (WIDTH/4-50<button.x and event.rel[0]<0) or (WIDTH*3/4-50>button.x and event.rel[0]>0):
                        button.move_ip((event.rel[0],0))
                    if button.x<WIDTH/4-50:
                        button.x=WIDTH/4-50
                    elif WIDTH*3/4-50<button.x:
                        button.x=WIDTH*3/4-50

        pygame.draw.rect(surface,(170,170,170) if button.collidepoint(mouse) else (100,100,100),button)
        pygame.draw.rect(surface, (255,255,255), [WIDTH/4-50,HEIGHT-80,WIDTH*3/4-150,5])
        pygame.draw.rect(surface, (255,255,255), [WIDTH/2-10,HEIGHT-90,20,20])

        font = pygame.font.SysFont(None, 24)
        img = font.render(f"time: {time:.1f} {'+' if 0<time_speed else ''}{time_speed:.2f}", True, (255,255,255))
        surface.blit(img, (20, 20))

        img = font.render("fps: "+str(fps), True, (255,255,255))
        surface.blit(img, (20, 50))

        for x in range(W):
            for y in range(H):
                if arr[int(time),x,y,0]!=0:
                    ceil=(x*SIZE+(WIDTH-S_WIDTH)/2,y*SIZE+(HEIGHT-S_HEIGHT)/2,SIZE,SIZE)
                if arr[int(time),x,y,0]==1:
                    pygame.draw.rect(surface, (255,0,0), ceil)
                elif arr[int(time),x,y,0]==2:
                    pygame.draw.rect(surface, (0,255,0), ceil)
                elif arr[int(time),x,y,0]==3:
                    pygame.draw.rect(surface, (0,0,255), ceil)
                
        pygame.display.flip()
        clock.tick(FPS)
        if 0<time_speed:
            time_speed*=2**((button.x-WIDTH/2+50)//(WIDTH/100)/25/(fps if fps else 1))
        else:
            time_speed/=2**((button.x-WIDTH/2+50)//(WIDTH-100)/25/(fps if fps else 1))
        time+=time_speed/(fps if fps else 1)
        if 0<time_speed<0.1:
            time_speed=-0.101
        elif 0>time_speed>-0.1:
            time_speed=0.101
        if len(arr)<=time:
            time=0
        elif time<0:
            time=len(arr)+time




pygame.init()

info = pygame.display.Info()
width, height=info.current_w-10,info.current_h-50
surface = pygame.display.set_mode((width,height), pygame.RESIZABLE)
mode=0
in_menu=True
while in_menu:
    surface.fill((0,0,0))
    mouse = pygame.mouse.get_pos()
    buttons=[
        [pygame.Rect(width/2-50,height/2-100,100,50),pygame.font.SysFont('Corbel',35).render('start',True,(255,255,255)),(width/2-30,height/2-90)],
        [pygame.Rect(width/2-50,height/2,100,50),pygame.font.SysFont('Corbel',35).render('watch',True,(255,255,255)),(width/2-40,height/2+10)],
        # [pygame.Rect(width/2-50,height/2+100,100,50),pygame.font.SysFont('Corbel',35).render('space',True,(255,255,255)),(width/2-40,height/2+110)]
    ]
    for ev in pygame.event.get():
        if ev.type == pygame.QUIT: 
            pygame.quit()
        if ev.type == pygame.MOUSEBUTTONDOWN:
            for num, button in enumerate(buttons):
                if button[0].collidepoint(mouse):
                    in_menu, mode=False, num
    for button in buttons:
        pygame.draw.rect(surface,(170,170,170) if button[0].collidepoint(mouse) else (100,100,100),button[0])
        surface.blit(*button[1:])
    pygame.display.update()

if mode==0:
    game()
elif mode==1:
    vising_mode(surface, width, height)
