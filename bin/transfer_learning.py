'''
    Helper file for transfer learning.
'''
import numpy as np

def qtableToDqn():
    def recurs(dimension:int, array:np.ndarray):

    recu


if __name__ == '__main__':
    arr:np.ndarray = np.load('q_table.npy')
    shp = (25, )+ arr.shape[1:]
    nw_arr = np.concatenate((arr, np.zeros(shp)))
    print(np.count_nonzero(arr))
    print(np.count_nonzero(nw_arr))
    np.save('q_table.npy', nw_arr)