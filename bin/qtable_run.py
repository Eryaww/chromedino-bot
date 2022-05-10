from collections import deque
import numpy as np

from environment import Environment, Dino

MEMORY_LEN = 10000
LR = 0.01
DISCOUNT_FACTOR = 0.95

if __name__ == '__main__':
    dino = Dino()
    q_table = np.load('q_table.npy')
    action_sequence = deque(maxlen=MEMORY_LEN)
    try:
        env = Environment()
        while True:
            state = env.get_state_v2(dino)
            action = np.argmax(q_table[state])

            env.render(dinos=[dino])
            state, reward, done = env.play_step_v2(dino, action)
            action_sequence.append((state, action, reward))
            if done:
                next_state = None
                # Keep learning from mistake, thats what makes you better and better
                # even in production :))
                while action_sequence:
                    state, action, reward = action_sequence.pop()
                    if next_state is None:
                        q_table[state][action] = reward
                    else:
                        q_table[state][action] += LR * (reward + DISCOUNT_FACTOR * np.max(q_table[next_state]) - q_table[state][action])
                    next_state = state
                env = Environment()
    finally:
        np.save('q_table.npy', q_table)
