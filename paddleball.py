import tkinter as tk
import random
import time
import subprocess
import sys

def restart_game():
    root.destroy()
    subprocess.Popen([sys.executable, 'paddleball.py'])


 
is_paused = False

def toggle_pause(event):
    global is_paused, pause_text
    
    if ball.hit_bottom:
        return
        
    is_paused = not is_paused
    
    if is_paused:
        pause_text = canvas.create_text(250, 150, text="Paused", font=('Arial', 30), fill="Green")
    else:
        canvas.delete(pause_text)
    
        game_loop()


class Ball:
    def __init__(self, canvas, paddle, color):
        self.canvas=canvas
        self.paddle=paddle
        self.id=canvas.create_oval(10, 10, 25, 25, fill=color)
        self.canvas.move(self.id, 245, 100)
        starts=[-3, -2, -1, 1, 2, 3]
        random.shuffle(starts)
        self.x = starts[0]    
        self.y = -3
        self.canvas_height=self.canvas.winfo_height()
        self.canvas_width=self.canvas.winfo_width()
        self.hit_bottom=False

    def hit_paddle(self, pos):
        paddle_pos = self.canvas.coords(self.paddle.id)
        if pos[2] >= paddle_pos[0] and pos[0]<= paddle_pos[2]:
            if pos[3] >= paddle_pos[1] and pos[3] <= paddle_pos[3]:
                return True
        return False

    def draw(self):
        self.canvas.move(self.id, self.x, self.y)
        pos=self.canvas.coords(self.id)
        if pos[1] <= 0:
            self.y=3
        if pos[3] >= self.canvas_height:
            self.hit_bottom = True
            canvas.create_text(250, 150, text="Game Over", font=('Arial', 30), fill="Red")
            
            restart_btn = tk.Button(root, text="Play Again", font=("Arial", 14), command=restart_game)
            self.canvas.create_window(250, 230, window=restart_btn)
            
        if self.hit_paddle(pos) == True:
            self.y = -3
        if pos[0] <= 0:
            self.x=3
        if pos[2] >=  self.canvas_width:
            self.x = -3

class Paddle:
    def __init__(self, canvas, color):
        self.canvas=canvas
        self.id=canvas.create_rectangle(0, 0, 100, 10, fill=color)
        self.canvas.move(self.id, 200, 300)
        self.x=0
        self.canvas_width=self.canvas.winfo_width()
        self.canvas.bind_all('<KeyPress-Left>', self.turn_left)
        self.canvas.bind_all('<KeyPress-Right>', self.turn_right)
    
    def draw(self):
        self.canvas.move(self.id, self.x, 0)
        pos=self.canvas.coords(self.id)
        if pos[0] <= 0:
            self.x=0
        elif pos[2] >= self.canvas_width:
            self.x=0

    def turn_left(self, evt):
        if not is_paused:
            self.x = -4

    def turn_right(self, evt):
        if not is_paused:
            self.x = 4

 
root=tk.Tk()
root.title("Game")
root.resizable(0,0)
root.wm_attributes("-topmost", 1)


canvas=tk.Canvas(root, width=500, height=400, bd=0, highlightthickness=0)
canvas.pack()
root.update()

paddle=Paddle(canvas, 'green')
ball=Ball(canvas, paddle, 'red')

root.bind_all('<KeyPress-space>', toggle_pause)


def game_loop():
    if ball.hit_bottom == False and is_paused == False:
        ball.draw()
        paddle.draw()
        root.after(15, game_loop)
    else:
        root.update()

 
game_loop()

root.mainloop()
