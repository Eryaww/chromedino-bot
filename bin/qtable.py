import numpy as np
import sys
import random
from typing import Tuple
from tqdm import tqdm

from environment import Environment, Dino


MEMORY_SIZE = 1500
LR = 0.01
DISCOUNT_FACTOR = 0.95

RENDER = False
if len(sys.argv) > 1:
    if '-r' in sys.argv:
        RENDER = True

if __name__ == '__main__':
    target_epoch = 10000
    q_table = np.load('q_table.npy')
    try:
        for epoch in tqdm(range(target_epoch), desc='On epoch'):
            env = Environment()
            dino = Dino()
            q_table = np.random.uniform(low=-2, high=0, size=(MEMORY_SIZE, MEMORY_SIZE, 3))
            score = 0
            
            while True:
                states:Tuple[int] = env.get_state(dino, return_int=True)
                # action = np.argmax(q_table[states])
                action = random.randint(0, 2)
                
                if RENDER:
                    env.render(dinos=[dino])
                died_dino, reward = env.play_step([dino], [action])
                
                if died_dino:
                    score = max(score, env.score)
                    q_table[states][action] = reward
                    break

                next_state = env.get_state(dino, return_int=True)
                current_q = q_table[states+tuple([action])]
                
                new_q = current_q + LR * (reward + DISCOUNT_FACTOR * np.max(q_table[next_state]) - current_q)
                q_table[states+tuple([action])] = new_q
    finally:
        np.save('q_table.npy', q_table)