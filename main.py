import twophase.solver as sv
import serial
from flask import Flask, render_template, redirect, url_for

class Cube:
    def __init__(self):
        self.cube = [['w', 'w', 'w', 'w', 'w', 'w', 'w', 'w'], ['o', 'o', 'o', 'o', 'o', 'o', 'o', 'o'], ['g', 'g', 'g', 'g', 'g', 'g', 'g', 'g'], ['r', 'r', 'r', 'r', 'r', 'r', 'r', 'r'], ['b', 'b', 'b', 'b', 'b', 'b', 'b', 'b'], ['y', 'y', 'y', 'y', 'y', 'y', 'y', 'y']]

    def faceMove(self, x):
        self.cube[x][0], self.cube[x][6], self.cube[x][4], self.cube[x][2] = self.cube[x][6], self.cube[x][4], self.cube[x][2], self.cube[x][0]
        self.cube[x][1], self.cube[x][7], self.cube[x][5], self.cube[x][3] = self.cube[x][7], self.cube[x][5], self.cube[x][3], self.cube[x][1]
        return
    def faceMovePrime(self, x):
        self.cube[x][0], self.cube[x][2], self.cube[x][4], self.cube[x][6] = self.cube[x][2], self.cube[x][4], self.cube[x][6], self.cube[x][0]
        self.cube[x][1], self.cube[x][3], self.cube[x][5], self.cube[x][7] = self.cube[x][3], self.cube[x][5], self.cube[x][7], self.cube[x][1]
        return

    def swap(self, x1, x2, x3, x4, y1, y2, y3, y4):
        self.cube[x1][y1], self.cube[x2][y2], self.cube[x3][y3], self.cube[x4][y4] = self.cube[x2][y2], self.cube[x3][y3], self.cube[x4][y4], self.cube[x1][y1]

    def cubeString(self):
        ret = []
        for face in [(0, 'w'), (3, 'r'), (2, 'g'), (5, 'y'), (1, 'o'), (4, 'b')]:
            for idx in [0, 1, 2, 7, 8, 3, 6, 5, 4]:
                ret.append(self.cube[face[0]][idx] if idx != 8 else face[1])
        
        ret = ''.join(ret)
        ret = ret.replace('w', 'U')
        ret = ret.replace('o', 'L')
        ret = ret.replace('g', 'F')
        ret = ret.replace('r', 'R')
        ret = ret.replace('b', 'B')
        ret = ret.replace('y', 'D')
        return ret


def move(cube, m, x):
    if m == 'U1':
        cube.faceMove(x)
        cube.swap(1,2,3,4,0,0,0,0)
        cube.swap(1,2,3,4,1,1,1,1)
        cube.swap(1,2,3,4,2,2,2,2)
    elif m == 'U3':
        cube.faceMovePrime(x)
        cube.swap(1,4,3,2,0,0,0,0)
        cube.swap(1,4,3,2,1,1,1,1)
        cube.swap(1,4,3,2,2,2,2,2)
    elif m == 'U2':
        move(cube, 'U1', x)
        move(cube, 'U1', x)
    elif m == 'D1':
        cube.faceMove(x)
        cube.swap(1,4,3,2,4,4,4,4)
        cube.swap(1,4,3,2,5,5,5,5)
        cube.swap(1,4,3,2,6,6,6,6)
    elif m == 'D3':
        cube.faceMovePrime(x)
        cube.swap(1,2,3,4,4,4,4,4)
        cube.swap(1,2,3,4,5,5,5,5)
        cube.swap(1,2,3,4,6,6,6,6)
    elif m == 'D2':
        move(cube, 'D1', x)
        move(cube, 'D1', x)
    elif m == 'R1':
        cube.faceMove(x)
        cube.swap(0,2,5,4,2,2,2,6)
        cube.swap(0,2,5,4,3,3,3,7)
        cube.swap(0,2,5,4,4,4,4,0)
    elif m == "R3":
        cube.faceMovePrime(x)
        cube.swap(0,4,5,2,2,6,2,2)
        cube.swap(0,4,5,2,3,7,3,3)
        cube.swap(0,4,5,2,4,0,4,4)
    elif m == 'R2':
        move(cube, 'R1', x)
        move(cube, 'R1', x)
    elif m == 'L1':
        cube.faceMove(x)
        cube.swap(0,4,5,2,6,2,6,6)
        cube.swap(0,4,5,2,7,3,7,7)
        cube.swap(0,4,5,2,0,4,0,0)
    elif m == 'L3':
        cube.faceMovePrime(x)
        cube.swap(0,2,5,4,6,6,6,2)
        cube.swap(0,2,5,4,7,7,7,3)
        cube.swap(0,2,5,4,0,0,0,4)
    elif m == 'L2':
        move(cube, 'L1', x)
        move(cube, 'L1', x)
    elif m == 'F1':
        cube.faceMove(x)
        cube.swap(0,1,5,3,4,2,0,6)
        cube.swap(0,1,5,3,5,3,1,7)
        cube.swap(0,1,5,3,6,4,2,0)
    elif m == 'F3':
        cube.faceMovePrime(x)
        cube.swap(0,3,5,1,4,6,0,2)
        cube.swap(0,3,5,1,5,7,1,3)
        cube.swap(0,3,5,1,6,0,2,4)
    elif m == 'F2':
        move(cube, 'F1', x)
        move(cube, 'F1', x)
    elif m == 'B1':
        cube.faceMove(x)
        cube.swap(0,3,5,1,0,2,4,6)
        cube.swap(0,3,5,1,1,3,5,7)
        cube.swap(0,3,5,1,2,4,6,0)
    elif m == 'B3':
        cube.faceMovePrime(x)
        cube.swap(0,1,5,3,0,6,4,2)
        cube.swap(0,1,5,3,1,7,5,3)
        cube.swap(0,1,5,3,2,0,6,4)
    elif m == 'B2':
        move(cube, 'B1', x)
        move(cube, 'B1', x)

cube = Cube()
moves = ['U', 'L', 'F', 'R', 'B', 'D']
s = serial.Serial("COM3", 115200);
app = Flask(__name__, template_folder='templates')

def move_serial(s):
    s.write(bytes(s[:2], 'utf-8'))

@app.route('/')
def index():
    return render_template('template.html')

@app.route("/move/<s>")
def mv(s):
    move(cube, s, moves.index(s[0]))
    move_serial(s)
    return redirect(url_for('index'))

@app.route('/solve')
def solve():
    global cube
    solved = sv.solve(cube.cubeString())
    print(solved)
    for m in solved.split()[:-1]:
        move(cube, m, moves.index(m[0]))
        move_serial(m)
        print(m)
    cube = Cube()
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)
