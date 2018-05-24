from enum import Enum
import random
import time
import threading
from getch import getch, pause
import pygame
from pygame.locals import *
from time import sleep

Status = Enum("Status", "NONE, WALL, ACTIVE, FIX")

BLOCKS = [
        [ [0, 1, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [0, 1, 1, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [1, 1, 0, 0], [0, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [1, 1, 1, 1], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [1, 1, 0, 0], [1, 1, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [1, 0, 0, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        [ [0, 0, 1, 0], [1, 1, 1, 0], [0, 0, 0, 0], [0, 0, 0, 0], ],
        ];

class Field:
    HEIGHT = 20
    WIDTH = 11
    DELETE_LINE = [ Status.WALL, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.FIX, Status.WALL]
    NEW_LINE = [ Status.WALL, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.NONE, Status.WALL]
    def __init__(self):
        self._field = self._initField();
        self._point = 0;

    def clear(self):
        for y in range(self.HEIGHT):
            for x in range(self.WIDTH):
                if self._field[y][x] == Status.ACTIVE:
                    self._field[y][x] = Status.NONE

    def write(self):
        print("\x1b[25D", self._point, "\x1b[25D")
        text = "\n\x1b[25D"
        for line in self._field:
            for l in line:
                if l == Status.WALL or l == Status.ACTIVE or l == Status.FIX:
                    text += "@ "
                else:
                    text += "_ "
            text += "\n\x1b[25D"
        print(text)

    def lineClear(self):
        for y in range(self.HEIGHT):
            if self._field[y] == self.DELETE_LINE:
                self._point += 1
                self._field.pop(y)
                self._field.insert(0, self.NEW_LINE)

    def gameFinish(self):
        return self._point >= 40

    def areBlock(self, pos):
        result = False
        for p in pos:
            if self._isBlock(p[0], p[1]):
                result = True

        return result

    def fix(self, pos):
        for p in pos:
            self._field[p[1]][p[0]] = Status.FIX

    def preFix(self, pos):
        for p in pos:
            self._field[p[1]][p[0]] = Status.ACTIVE

    def _initField(self):
        field = []
        for y in range(self.HEIGHT):
            line = []
            for x in range(self.WIDTH):
                if x == 0 or x == self.WIDTH - 1 or y == self.HEIGHT - 1:
                    line.append(Status.WALL)
                else:
                    line.append(Status.NONE)
            field.append(line)
        return field

    def _isBlock(self, x, y):
        return self._field[y][x] == Status.WALL or self._field[y][x] == Status.FIX


class Current:
    def __init__(self, x, y, block = None):
        self._x = x
        self._y = y
        if block == None:
            self._current = self._newBlock()
        else:
            self._current = block

    def movePosition(self):
        b_pos = []
        for y in range(4):
            for x in range(4):
                if self._current[y][x] == 1:
                    b_pos.append([self._x + x, self._y + y])
        return b_pos


    def right(self):
        return Current(self._x + 1, self._y, self._current)

    def left(self):
        return Current(self._x - 1, self._y, self._current)

    def fall(self):
        return Current(self._x, self._y + 1, self._current)

    def rotation(self):
        tmp = [[0 for i in range(4)] for j in range(4)]
        for i in range(4):
            for j in range(4):
                tmp[j][i] = self._current[i][j]
        for i in range(4):
            tmp[i].reverse()
        return Current(self._x, self._y, tmp)

    def _newBlock(self):
        return random.choice(BLOCKS)


class InputThread(threading.Thread):
    def __init__(self):
        super(InputThread, self).__init__()
        self._cmd = 'n'

    def run(self):
        i = 0
        while True:
            key = getch()
            self._cmd = key
            if key == 'q':
                break

    def getCmd(self):
        return self._cmd

    def resetCmd(self):
        self._cmd = 'n'


def displayClear():
    print("\x1b[2J\x1b[0;0H" ,end="")

def main():
    displayClear()

    field = Field()
    field.write()

    current = Current(5, 0)

    th = InputThread()
    th.start()

    pygame.init()

    while True:
        time.sleep(0.1)
        displayClear()
        print("left: →, right: ←, rotate:↑ space, q: break \x1b[25D")
        
        #コントローラーの動作を取得
        eventlist = pygame.event.get()
        eventlist = filter(lambda e : e.type == pygame.locals.JOYBUTTONDOWN , eventlist)
        joykey = list(map(lambda x : x.button,eventlist))

        if len(joykey) > 0 and joykey[0] == int(2):
            tmp = current.left()
        elif len(joykey) > 0 and joykey[0] == int(1):
            tmp = current.right()
        elif len(joykey) > 0 and joykey[0] == int(3):
            tmp = current.rotation()
        else:
            tmp = current.fall()
        next_pos = tmp.movePosition()
        
        if not field.areBlock(next_pos):
            field.preFix(next_pos)
            current = tmp
        elif th.getCmd() != 'n':
            current = current
        else:
            current_pos = current.movePosition()
            field.fix(current_pos)
            current = Current(5, 0)
            next_pos = current.movePosition()
            if field.areBlock(next_pos):
                print("game over")
                break
        field.write()
        field.clear()
        field.lineClear()
        th.resetCmd()
        if field.gameFinish():
            print("success!!!!!!")
            break
        
if __name__ == '__main__':
    pygame.joystick.init()
    try:
        joys = pygame.joystick.Joystick(0)
        joys.init()
        main()
    except pygame.error:
        print('error has accured')
