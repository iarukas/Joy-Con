import pygame
from pygame.locals import *
from time import sleep
import time
 
def main() :
    """pygame.joystick.init()
    joystick0 = pygame.joystick.Joystick(0)
    joystick0.init()
    """
    pygame.init()
    while True:
 
        # コントローラーの操作を取得
        eventlist = pygame.event.get()
        """
        for e in eventlist:
            if e.type == QUIT:
                return

            if e.type == pygame.locals.JOYAXISMOTION:
                x, y = joystick0.get_axis(0), joystick0.get_axis(1)
                print ('axis x:' + str(x) + ' axis y:' + str(y))
            elif e.type == pygame.locals.JOYHATMOTION:
                
                x, y = joystick0.get_hat(0)
                print ('hat x:' + str(x) + ' hat y:' + str(y))
            elif e.type == pygame.locals.JOYBUTTONDOWN:
                print ('button:' + str(e.button))
        """
        # 操作の中からボタンを押したときだけに絞り込む
        eventlist = filter(lambda e : e.type == pygame.locals.JOYBUTTONDOWN , eventlist)
 
        # ボタン入力の読み込みを表示
        
        key=list(map(lambda x : x.button,eventlist))
        #print(key)
        if len(key) > 0:
            print(key)
            #0,←,1,↓,2,↑,3,→
            if key[0] == int(0):break
            elif key[0] == int(1):break
            elif key[0] == int(2):break
            elif key[0] == int(3):break

        sleep(0.1)
 
if __name__ == '__main__':
    pygame.joystick.init()
    try:
       joys = pygame.joystick.Joystick(0)
       joys.init()
       main()
    except pygame.error:
        print( 'error has occured')
    


