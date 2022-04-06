from agent import *
from layout import *
import matplotlib.pyplot as plt
size = 10
num_snakes = 1
# players = 1
players = [RandomPlayer(0)]
gui_size = 600

# game = Game(size, num_snakes, players, gui=None, display=True, max_turns=100)
# gui = Gui(game, gui_size)
# game.play(True, terminate=False)

population_size = 100
num_generations = 500
num_trails = 1
window_size = 10   #Board seen by the agent NxN
hidden_size = 50   #Brain SIze neurons
board_size = 15
counter = []
agent = Player(population_size, num_generations, num_trails, window_size, hidden_size, board_size, counter, mutation_chance=0.2, mutation_size=0.3)
agent.evolve()
x = list(range(num_generations))
plt.plot(x, counter)
plt.xlabel('Generations')
plt.ylabel('Max Score')
plt.show()