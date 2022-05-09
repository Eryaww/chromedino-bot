# Chrome Dino Bot
## Sceme
- Neural Network Input for NEAT algorithm
1. Distance from top to top ( Dino to Closest Object)
2. Distance from bottom to bottom ( Dino to Closest Object)
- Neural Network Output for NEAT algorithm
1. Stay
2. Jump
3. Crawl
- Reward Scheme for NEAT algorithm
1. Time of surviving
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