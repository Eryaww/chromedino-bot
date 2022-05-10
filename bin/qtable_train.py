from collections import deque
import queue
import numpy as np
import sys
import random
from typing import Tuple
from tqdm import tqdm

from environment import Environment, Dino


MEMORY_SIZE = 100000
TABLE_SIZE = 1000
LR = 0.01
DISCOUNT_FACTOR = 0.95

RENDER = False
if len(sys.argv) > 1:
    if '-r' in sys.argv:
        RENDER = True

if __name__ == '__main__':
    target_epoch = 1000000
    q_table = np.load('q_table.npy')
    try:
        for epoch in tqdm(range(target_epoch), desc='On epoch'):
            env = Environment()
            dino = Dino()
            score = 0
            move_sequence = deque(maxlen=MEMORY_SIZE)
            
            while True:
                state:Tuple[int, int, int, int] = env.get_state_v2(dino)
                # if random.randint(0, 100) <= 100:
                action = np.argmax(q_table[state])
                # else:
                #     action = random.randint(0, 2)
                
                if RENDER:
                    env.render(dinos=[dino])
                next_state, reward, done = env.play_step_v2(dino, action)
                
                move_sequence.append((state, action, reward))
                if done:
                    score = max(score, env.score)
                    next_state = None
                    # Back Propagation
                    while move_sequence:
                        state, action, reward = move_sequence.pop()
                        if next_state is None:
                            q_table[state][action] = reward
                        else:
                            q_table[state][action] += LR * (reward + DISCOUNT_FACTOR * np.max(q_table[next_state]) - q_table[state][action])
                        next_state = state
                    break
    finally:
        np.save('q_table.npy', q_table)