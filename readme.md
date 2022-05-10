# Chrome Dino Bot
## Codebase
The code using here is smelly and not built using good OOP concept, I might update this in the future
## Sceme
- Game State
1. Distance from top to top ( Dino to Closest Object)
2. Distance from bottom to bottom ( Dino to Closest Object)
- Game Action
1. Stay
2. Jump
3. Crawl
- Reward
1. Time of surviving for Genetic Algorithm
2. Object that has been passed by for Q Learning
## File Description
- environment.py (Contain the environment interface which is the game)
- neat_evolve.py (Run evolutionary algorithm and save the best agent as best.pickle)
- neat_run.py (Run the game with best.pickle as agent)
## How to Run
- Make sure python and pip is installed
- Install required library using pip
```
    pip install -r requirements.txt
```
- Activate virtual environment
- run the script inside bin