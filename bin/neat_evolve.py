import os
import neat
import numpy as np
import pickle
from environment import Dino, Environment

# HYPERPARAM
RENDER = True

config_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'neat-config.txt')

def evolve(genome, config):
    # genome = inx:int, gen:DefaultGenome
    nets:list[neat.nn.FeedForwardNetwork] = []
    individual:list[neat.DefaultGenome] = []
    dinos = []
    for inx, gen in genome:
        nets.append(neat.nn.FeedForwardNetwork.create(gen, config))
        gen.fitness = 0
        dinos.append(Dino())
        individual.append(gen)
    done = False
    env = Environment(debug_mode=True)
    while not done:
        act = []
        for inx, net in enumerate(nets):
            act.append(np.argmax(net.activate(inputs=(env.get_state(dinos[inx]))))) # [stay, jump, crawl]
        # Reward is not used since we are not using a Q-table
        died_dinos, _ = env.play_step(dinos, act)
        for dino in died_dinos:
            inx = dinos.index(dino)
            dinos.pop(inx)
            nets.pop(inx)
        for inx, dino in enumerate(dinos):
            individual[inx].fitness += 1
            if individual[inx].fitness >= 5000:
                print("SAVE THE INDIVIDUAL? Y/N")
                res = input()
                if res == "Y" or res == 'y':
                    with open('best.pickle', 'wb') as f:
                        pickle.dump(nets[inx], f)
                    print("SAVED")
                    return
        if not dinos:
            done = True
        # TODO FIX RENDER ARGS
        if RENDER:
            env.render(dinos)

def run():
    config = neat.Config(
        neat.DefaultGenome, 
        neat.DefaultReproduction,
        neat.DefaultSpeciesSet,
        neat.DefaultStagnation,
        config_file
    )
    population = neat.Population(config)
    population.add_reporter(neat.StdOutReporter(True))
    population.add_reporter(neat.StatisticsReporter())
    
    winner = population.run(evolve)

    print("SAVE THE INDIVIDUAL? Y/N")
    res = input()
    if res == "Y" or res == 'y':
        with open('best.pickle', 'wb') as f:
            pickle.dump(winner, f)
        print("SAVED")

if __name__ == '__main__':
    run()