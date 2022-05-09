import os
import neat
import pickle
import numpy as np
from environment import Environment, Dino

config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'neat-config.txt')

if __name__ == '__main__':
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    with open('best.pickle', 'rb') as f:
        net:neat.nn.FeedForwardNetwork = pickle.load(f)
    env = Environment()
    done = False
    dino = Dino()
    # net = neat.nn.FeedForwardNetwork.create(gen, config)
    while not done:
        output = net.activate(env.get_state(dino=dino))
        dead_dino = env.play_step([dino], [np.argmax(output)])
        env.render([dino])
        if dead_dino:
            inp = input()
            break