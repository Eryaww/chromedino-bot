import numpy as np
import tensorflow.keras as keras
from environment import Environment, Dino

if __name__ == '__main__':
    model:keras.Model = keras.models.load_model('dqn.h5')
    env = Environment()
    dino = Dino()
    while True:
        state = np.array(env.get_state_v2(dino)).reshape((1, 3))
        pred = model.predict(state)
        action = np.argmax(pred)
        env.render(dinos=[dino])
        state, reward, done = env.play_step_v2(dino, action)
        if done:
            env = Environment()
            dino = Dino()