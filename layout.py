import tkinter as tk
import numpy as np
import time as time
import random

UP = (-1,0)
DOWN = (1,0)
RIGHT = (0,1)
LEFT = (0,-1)
MOVES = [UP,DOWN,LEFT,RIGHT]
EMPTY = 0
FOOD = 99

food_generation = [(random.randint(0,9), random.randint(0,9)) for i in range(200)]
class Game:
    def __init__(self, size, num_snakes, players, gui=None, display=False, max_turns=100):
        self.size = size
        self.num_snakes = num_snakes
        self.players = players
        self.gui = gui
        self.display = display
        self.max_turns = max_turns

        self.num_food = 2
        self.turn = 0
        self.snake_size = 3

        self.snake = [[((j+1)*self.size//(2*num_snakes),self.size//2 + i) for i in range(self.snake_size)] for j in range(self.num_snakes)]
        # self.food = [(self.size//4, self.size//4), (3*self.size//4, self.size//4), (self.size//4, 3*self.size//4), (3*self.size//4, 3*self.size//4)]
        self.food = [(3*self.size//4, self.size//4) ]

        self.player_id = [i for i in range(self.num_snakes)]
        self.board = np.zeros([self.size, self.size])
        for i in self.player_id:
            for tup in self.snake[i]:
                self.board[tup[0]][tup[1]] = i+1
        for tup in self.food:
            self.board[tup[0]][tup[1]] = FOOD

        self.food_index = 0
        self.food_xy = food_generation


#   ########-> head[-1]...L-R       move - i++, h++...tail--not if eat
    def move(self):
        moves = []
        # head
        for i in self.player_id:
            snake_i = self.snake[i]
            move_i = self.players[i].get_move(self.board, snake_i)
            moves.append(move_i)
            new_square = (snake_i[-1][0] + move_i[0], snake_i[-1][1]+move_i[1])
            snake_i.append(new_square)
        # tail
        for i in self.player_id:
            head_i = self.snake[i][-1]
            # eats....last element of ith snake as null
            if head_i not in self.food:
                self.board[self.snake[i][0][0]][self.snake[i][0][1]] = EMPTY
                self.snake[i].pop(0)
            else:
                self.food.remove(head_i)
        # out
        for i in self.player_id:
            head_i = self.snake[i][-1]          #tail Upd
            if head_i[0] >= self.size or head_i[1] >= self.size or head_i[0] < 0 or head_i[1] < 0:
                self.player_id.remove(i)
            else:
                self.board[head_i[0]][head_i[1]] = i+1
        #collisions
        for i in self.player_id:
            head_i = self.snake[i][-1]
            for j in range(self.num_snakes):
                if i==j:
                    # crashing into self 
                    if head_i in self.snake[i][:-1]:
                        self.player_id.remove(i)
                else:
                    if head_i in self.snake[j]:
                        self.player_id.remove(i)
        
        # update food
        while len(self.food) < self.num_food:
            x = self.food_xy[self.food_index][0]
            y = self.food_xy[self.food_index][1]   # next food index
            # while self.food_xy
            while self.board[x][y] != EMPTY:                #square isn empty
                self.food_index += 1
                x = self.food_xy[self.food_index][0]
                y = self.food_xy[self.food_index][1] 
            self.food.append((x,y))
            self.board[x][y] = FOOD
            self.food_index += 1
            
        return moves

    def play(self, display, terminate=False):
        # terminate condition is to kill a snake that does not eats food....saves us time rather than assigning penalty for that
        if display:
            self.display_board()
        while(True):
            if terminate:
                for i in self.player_id:
                    if len(self.snake[0])-self.turn/20 <= 0:            #20 is a const..checks if snake is eating per const numner of turns
                        self.player_id.remove(i)
                        # return condtion -2 is for a single snake
                        return -2
            if len(self.player_id) == 0:
                return -1
            # game over condition
            if self.turn >= self.max_turns:
                return 0
            moves = self.move()
            self.turn += 1

            if display:
                for i in moves:
                    if i == UP:
                        print('UP')
                    elif i == DOWN:
                        print('DOWN')
                    elif i == RIGHT:
                        print('RIGHT')
                    else:
                        print('LEFT')
                
                self.display_board()
                # self.gui.update()
                if self.gui is not None:
                    self.gui.update()

                time.sleep(0.1)

    
    def display_board(self):
        for i in range(self.size):
            for j in range(self.size):
                if self.board[i][j] == EMPTY:
                    print('_|', end="")
                elif self.board[i][j] == FOOD:
                    print('F|', end="")
                else:
                    print(str(int(self.board[i][j]))+'|', end="")
            print("|")

class Gui:

    def __init__(self, game, size):
        self.game = game
        self.game.gui = self
        self.size = size
        
        self.ratio = self.size/self.game.size
        
        self.app = tk.Tk()
        # self.app.configure(background='black')
        self.canvas = tk.Canvas(self.app, width=self.size, height=self.size)
        self.canvas.configure(bg='black')
        self.canvas.pack()

        for i in range(len(self.game.snake)):
            # color = '#' + '{0:03X}'.format((i+1)*500)
            color = '#F71203'
            snake = self.game.snake[i]
            self.canvas.create_oval(self.ratio*(snake[-1][1]), self.ratio*(snake[-1][0]), self.ratio*(snake[-1][1] +1), self.ratio*(snake[-1][0] + 1), fill=color)

            for j in range(len(snake)-1):
                color = '#' + '{0:03X}'.format((i+1)*125)
                self.canvas.create_oval(self.ratio*(snake[j][1]), self.ratio*(snake[j][0]), self.ratio*(snake[j][1] +1), self.ratio*(snake[j][0] + 1), fill=color)
        
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio*(food[1]), self.ratio*(food[0]), self.ratio*(food[1] +1), self.ratio*(food[0] + 1), fill='#000000')


    def update(self):
        self.canvas.delete("all")
        for i in range(len(self.game.snake)):
            # color = '#' + '{0:03X}'.format((i+1)*500)
            color = '#F71203'
            snake = self.game.snake[i]
            self.canvas.create_oval(self.ratio*(snake[-1][1]), self.ratio*(snake[-1][0]), self.ratio*(snake[-1][1] +1), self.ratio*(snake[-1][0] + 1), fill=color)

            for j in range(len(snake)-1):
                color = '#' + '{0:03X}'.format((i+1)*125)
                self.canvas.create_oval(self.ratio*(snake[j][1]), self.ratio*(snake[j][0]), self.ratio*(snake[j][1] +1), self.ratio*(snake[j][0] + 1), fill=color)
        
        for food in self.game.food:
            self.canvas.create_rectangle(self.ratio*(food[1]), self.ratio*(food[0]), self.ratio*(food[1] +1), self.ratio*(food[0] + 1), fill='#03F724')
        
        self.canvas.pack()
        self.app.update()