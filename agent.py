# from _typeshed import Self
from layout import *
import math

class RandomPlayer:

    def __init__(self, i):
        self.i = i

    def get_move(self, board, snake):
        r = random.randint(0,3)
        return MOVES[r]

# r = random.randint(0,3)
# print(type(MOVES[r]))


# change Later
class Player():

    def __init__(self, population_size, num_generations, num_trails, window_size, hidden_size, board_size, counter, mutation_chance=0.2, mutation_size=0.3):
        self.population_size = population_size
        self.num_generations = num_generations
        self.num_trails = num_trails
        
        self.window_size = window_size
        self.hidden_size = hidden_size
        self.board_size = board_size

        self.mutation_chance = mutation_chance
        self.mutation_size = mutation_size
        self.counter = counter
        
        self.display = False

        self.current_brain = None
        self.population = [self.NN(self.window_size**2, self.hidden_size, len(MOVES)) for g in range(self.population_size)]

    def NN(self, input_size, hidden_size, output_size):
        hidden_layer1 = np.array([[random.uniform(-1,1) for i in range(input_size+1)] for j in range(hidden_size)])
        # hidden_layer2 = np.array([[random.uniform(-1,1) for i in range(input_size+1)] for j in range(input_size)])
        hidden_layer2 = np.array([[random.uniform(-1,1) for i in range(hidden_size+1)] for j in range(hidden_size)])
        output_layer = np.array([[random.uniform(-1,1) for i in range(hidden_size+1)] for j in range(output_size)])
        # output_layer = np.array([[random.uniform(-1,1) for i in range(input_size+1)] for j in range(hidden_size)])

        return[hidden_layer1, hidden_layer2, output_layer]
    
    def get_move(self, board, snake):
        input_vector = self.process_board(board, snake[-1][0], snake[-1][1], snake[-2][0], snake[-2][1])
        hidden_layer1 = self.current_brain[0]
        hidden_layer2 = self.current_brain[1]
        output_layer = self.current_brain[2]

        # forward prop ............. row-wise
        hidden_result1 = np.array([math.tanh(np.dot(input_vector, hidden_layer1[i])) for i in range(hidden_layer1.shape[0])] + [1])
        hidden_result2 = np.array([math.tanh(np.dot(hidden_result1, hidden_layer2[i])) for i in range(hidden_layer2.shape[0])] + [1])
        output_result = np.array([np.dot(hidden_result2, output_layer[i]) for i in range(output_layer.shape[0])])

        max_index = np.argmax(output_result)
        return MOVES[max_index]

    # input is the cells surrounding the head minus the body and walls(if near)
    def process_board(self, board, x1, y1, x2, y2):
        input_vector = [[0 for i in range(self.window_size)] for j in range(self.window_size)]

        for i in range(self.window_size):
            for j in range(self.window_size):
                ii = x1 + i - self.window_size//2
                jj = y1 + j - self.window_size//2

                if ii<0 or jj<0 or ii>= self.board_size or jj>=self.board_size:
                    input_vector[i][j] = -1
                elif board[ii][jj] == FOOD:
                    input_vector[i][j] = 1
                elif board[ii][jj] == EMPTY:
                    input_vector[i][j] = 0
                else:
                    input_vector[i][j] = -1
        # metadata
        if self.display:
            print(np.array(input_vector))
        input_vector = list(np.array(input_vector).flatten())+[1]    # add .flatten function here

        return np.array(input_vector)

    def reproduce(self,top_25):
        new_population = []
        for brain in top_25:
            new_population.append(brain)
        for brain in top_25:
            new_brain = self.mutate(brain)
            new_population.append(new_brain)
# random
        for i in range(self.population_size//2):
            new_population.append(self.NN(self.window_size**2, self.hidden_size, len(MOVES)))
        
        return new_population

    def mutate(self, brain):
        # copy the matrix/layer and make small mutations
        new_brain = []
        for layer in brain:
            new_layer = np.copy(layer)
            for i in range(new_layer.shape[0]):
                for j in range(new_layer.shape[1]):
                    if random.uniform(0,1) < self.mutation_chance:
                        new_layer[i][j] += random.uniform(-1,1)*self.mutation_size

            new_brain.append(new_layer)
        return new_brain

    def one_generation(self):
        scores = [0 for i in range(self.population_size)]
        max_score = 0
        for i in range(self.population_size):
            for j in range(self.num_trails):
                self.current_brain = self.population[i]
                game = Game(self.board_size, 1, [self])
                outcome = game.play(False, terminate=True)
                score = len(game.snake[0])
                scores[i] += score
                if outcome == 0:
                    print('Snake ', i, ' made it to the last turn')
                if score > max_score:
                    max_score = score
                    print(max_score, ' at ID ', i)

        top_25_indexes = list(np.argsort(scores))[3*(self.population_size//4):self.population_size]
        print(scores)
        top_25 = [self.population[i] for i in top_25_indexes][::-1]
        self.counter.append(scores[0])
        self.population = self.reproduce(top_25)

    def evolve(self):
        for i in range(self.num_generations):
            self.one_generation()
            print("Generation ", i)

        key = input("Enter any character to display boards")
        for brain in self.population:
            self.display = True
            self.current_brain = brain
            game = Game(self.board_size, 1, [self], display=True)
            gui = Gui(game, 800)
            game.play(True, terminate=True)
