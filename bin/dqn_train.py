from collections import deque
import os
import queue
import random
from environment import Environment, Dino
from typing import Tuple
import numpy as np
import tensorflow as tf
import tensorflow.keras as keras
from keras import layers, activations, optimizers, losses
import tqdm

def get_model() -> keras.Model:
    model = keras.Sequential([
        layers.Dense(64),
        layers.Dense(128),
        layers.Dense(256),
        layers.Dense(128),
        layers.Dense(64),
        layers.Dense(3)
    ])
    model.compile(optimizer='adam', metrics=['accuracy'], loss=losses.MSE)
    return model

def train_from_qtable(model:keras.Model):
    q_table = np.load('q_table.npy')
    train = []
    target = []
    for state1 in range(q_table.shape[0]):
        for state2 in range(q_table.shape[1]):
            for state3 in range(q_table.shape[2]):
                train.append(np.array([state1, state2, state3]))
                target.append(q_table[state1, state2, state3])
    train, target =  np.array(train), np.array(target)
    model.fit(train, target, epochs=10, batch_size=1024, shuffle=True)
    model.save('dqn.h5')
    return model

class DQNAgent:
    def __init__(self, model:keras.Model) -> None:
        self.model:keras.Model = model
        self.memory = deque(maxlen=1_000_000)
    
    def train_step(self):
        train, target = [], []
        last_pred = None
        for state, action, next_state, reward, done in reversed(self.memory):
            pred = self.model.predict(np.array(state).reshape(1, 3))[0]
            if done:
                pred[action] = reward
            else:
                if last_pred is None:
                    continue
                max_future_q = np.max(last_pred)
                pred[action] = pred[action] + 0.1 * ( reward + 0.95 * max_future_q - pred[action] )

            train.append(state)
            target.append(pred)
            last_pred = pred
        self.memory.clear()
        self.model.fit(np.array(train), np.array(target), epochs=10, batch_size=64, shuffle=True, verbose=0)

    def train(self):
        for epoch in tqdm.tqdm(range(1_000), desc='Training'):
            dino = Dino()
            env = Environment()
            while True:
                if random.randint(0, 100) < 70:
                    action = np.argmax(self.model.predict(np.array(env.get_state_v2(dino)).reshape(1, 3)))
                else:
                    action = random.randint(0, 2)
                state = env.get_state_v2(dino)
                next_state, reward, done = env.play_step_v2(dino, action)
                self.memory.append((state, action, next_state, reward, done))
                
                if done:
                    break
            self.train_step()

if __name__ == '__main__':
    # model = get_model()
    model:keras.Model = keras.models.load_model('dqn.h5')
    dqn = DQNAgent(model)
    try:
        dqn.train()
    finally:
        dqn.model.save('dqn.h5')
